"""Lossless single-line SRT conversion, page guides and timeline validation.

Python standard library only. Input files are never overwritten.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

TIME = r'\d{2,}:\d{2}:\d{2},\d{3}'
TIMING = re.compile(rf'^({TIME})\s*-->\s*({TIME})(?:\s+.*)?$')


def milliseconds(value):
    hours, minutes, seconds, fraction = map(int, re.split(r'[:,]', value))
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f'Invalid timestamp: {value}')
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + fraction


def stamp(value):
    hours, remainder = divmod(int(value), 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, fraction = divmod(remainder, 1000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{fraction:03d}'


def parse_srt(path):
    text = Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    if not text.strip():
        raise ValueError('Empty subtitle file')
    blocks = re.split(r'\n[ \t]*\n+', text.strip())
    cues = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError('Expected index, timing and text in each SRT block')
        match = TIMING.fullmatch(lines[1].strip())
        if not match:
            raise ValueError(f'Invalid timing line: {lines[1]}')
        start, end = [milliseconds(t) for t in match.groups()]
        index = int(lines[0].strip())
        if cues and index != cues[-1]['index'] + 1:
            raise ValueError('Subtitle indexes are not consecutive')
        if not 0 <= start < end:
            raise ValueError(f'Invalid duration in cue {index}')
        if cues and start < cues[-1]['end_ms']:
            raise ValueError(f'Overlapping or unordered cue {index}')
        cues.append({'index': index, 'index_line': lines[0], 'timing': lines[1],
                     'start_ms': start, 'end_ms': end, 'lines': lines[2:]})
    return cues


def render(cues):
    return '\n\n'.join('\n'.join([c['index_line'], c['timing'], *c['lines']]) for c in cues) + '\n\n'


def write_output(path, text, inputs, force=False):
    output = Path(path).resolve()
    if output in [Path(p).resolve() for p in inputs]:
        raise ValueError('Output must differ from every input path')
    if output.exists() and not force:
        raise ValueError('Output exists; choose a new path or explicitly pass --force')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding='utf-8-sig')
    return output


def report(cues):
    return {'cues': len(cues), 'first_seconds': cues[0]['start_ms'] / 1000,
            'last_seconds': cues[-1]['end_ms'] / 1000,
            'max_text_lines': max(len(c['lines']) for c in cues),
            'max_line_characters': max(len(line) for c in cues for line in c['lines']),
            'words': sum(len(' '.join(c['lines']).split()) for c in cues)}


def single_line(args):
    original = parse_srt(args.input)
    converted = [{**cue, 'lines': [' '.join(line.strip() for line in cue['lines'])]} for cue in original]
    # Verify the meaningful invariants before writing, rather than assuming joins are harmless.
    for before, after in zip(original, converted):
        if before['timing'] != after['timing'] or before['index_line'] != after['index_line']:
            raise ValueError('Conversion changed index or timing')
        if ' '.join(before['lines']).split() != after['lines'][0].split():
            raise ValueError('Conversion changed subtitle wording')
    output = write_output(args.output, render(converted), [args.input], args.force)
    print(json.dumps({'output': str(output), **report(converted),
                      'wording_and_timing_preserved': True}, ensure_ascii=False, indent=2))


def page_guides(args):
    path = Path(args.timings)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as source:
            pages = list(csv.DictReader(source))
    else:
        pages = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(pages, list) or not pages:
        raise ValueError('Page timing file must contain a nonempty list')
    cues = []
    for number, page in enumerate(pages, 1):
        if int(page['slide']) != number:
            raise ValueError('Pages must be numbered consecutively from 1')
        start = round(float(page['start_seconds']) * 1000)
        end = round(float(page['end_seconds']) * 1000)
        if not 0 <= start < end:
            raise ValueError(f'Invalid page interval {number}')
        if not cues and start != 0:
            raise ValueError('Page timeline must begin at zero')
        if cues and start != cues[-1]['end_ms']:
            raise ValueError('Page intervals must be contiguous after millisecond rounding')
        cues.append({'index': number, 'index_line': str(number),
                     'timing': f'{stamp(start)} --> {stamp(end)}',
                     'start_ms': start, 'end_ms': end,
                     'lines': [f'PPT {number:02d} / {len(pages)}']})
    output = write_output(args.output, render(cues), [args.timings], args.force)
    print(json.dumps({'output': str(output), **report(cues)}, ensure_ascii=False, indent=2))


def validate(args):
    cues = parse_srt(args.input)
    if args.max_lines is not None and any(len(c['lines']) > args.max_lines for c in cues):
        raise ValueError('Subtitle text exceeds the specified line count')
    if args.audio_seconds is not None and cues[-1]['end_ms'] > round(args.audio_seconds * 1000):
        raise ValueError('Subtitles extend beyond audio')
    if args.transcript:
        transcript = Path(args.transcript).read_text(encoding='utf-8-sig').split()
        subtitle_words = ' '.join(' '.join(c['lines']) for c in cues).split()
        if transcript != subtitle_words:
            raise ValueError('Subtitle words differ from the transcript')
    print(json.dumps({'valid': True, **report(cues)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    one = commands.add_parser('single-line', help='Join text lines only; preserve cue timing and words')
    one.add_argument('--input', required=True)
    one.add_argument('--output', required=True)
    one.add_argument('--force', action='store_true')
    one.set_defaults(run=single_line)
    guides = commands.add_parser('page-guides', help='Build one full-duration subtitle block per PPT page')
    guides.add_argument('--timings', required=True)
    guides.add_argument('--output', required=True)
    guides.add_argument('--force', action='store_true')
    guides.set_defaults(run=page_guides)
    check = commands.add_parser('validate', help='Check syntax, ordering, overlaps and optional coverage')
    check.add_argument('--input', required=True)
    check.add_argument('--max-lines', type=int)
    check.add_argument('--audio-seconds', type=float)
    check.add_argument('--transcript')
    check.set_defaults(run=validate)
    args = parser.parse_args()
    try:
        args.run(args)
    except (ValueError, OSError, KeyError, TypeError, OverflowError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
