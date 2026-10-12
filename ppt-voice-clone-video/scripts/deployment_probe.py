"""Probe a Windows/CUDA Chatterbox environment without loading model weights."""
import argparse
import importlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', choices=['cuda', 'cpu'], default='cuda')
    parser.add_argument('--ffmpeg', help='Absolute FFmpeg executable, or resolve it from PATH')
    parser.add_argument('--output', required=True, help='JSON diagnostic report')
    args = parser.parse_args()
    result = {'python': sys.version, 'executable': sys.executable,
              'platform': platform.platform(), 'device_requested': args.device, 'checks': {}}

    def check(name, work):
        try:
            result['checks'][name] = {'passed': True, 'result': work()}
        except Exception as exc:
            result['checks'][name] = {'passed': False, 'error': f'{type(exc).__name__}: {exc}'}

    def compute():
        import torch
        if args.device == 'cuda':
            if not torch.cuda.is_available():
                raise RuntimeError('CUDA unavailable: check driver and installed torch variant')
            # Visibility is insufficient: perform real allocation and kernels.
            answer = (torch.ones(4, device='cuda') * 2).sum().item()
            return {'torch': torch.__version__, 'cuda_runtime': torch.version.cuda,
                    'gpu': torch.cuda.get_device_name(), 'capability': torch.cuda.get_device_capability(),
                    'compiled_arches': torch.cuda.get_arch_list(), 'kernel_answer': answer}
        return {'torch': torch.__version__, 'kernel_answer': (torch.ones(4) * 2).sum().item()}

    def spectrogram():
        import torch
        import torchaudio
        return {'torchaudio': torchaudio.__version__,
                'shape': list(torchaudio.transforms.Spectrogram()(torch.ones(24000)).shape)}

    def kaldi():
        import torch
        from torchaudio.compliance.kaldi import fbank
        return list(fbank(torch.rand(1, 16000), num_mel_bins=80).shape)

    def chatterbox():
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        return {'class': ChatterboxTurboTTS.__name__,
                'has_from_local': callable(getattr(ChatterboxTurboTTS, 'from_local', None))}

    def ffmpeg():
        binary = args.ffmpeg or shutil.which('ffmpeg')
        if not binary:
            raise RuntimeError('FFmpeg not found: supply --ffmpeg or add its directory to PATH')
        kwargs = {'creationflags': 0x08000000} if sys.platform == 'win32' else {}
        process = subprocess.run([str(binary), '-version'], check=True, capture_output=True,
                                 text=True, encoding='utf-8', errors='replace', timeout=20, **kwargs)
        return {'executable': str(binary), 'version': process.stdout.splitlines()[0]}

    check('compute', compute)
    check('spectrogram', spectrogram)
    check('kaldi_fbank', kaldi)
    check('chatterbox_import', chatterbox)
    check('soundfile_import', lambda: importlib.import_module('soundfile').__version__)
    check('ffmpeg', ffmpeg)
    result['passed'] = all(item['passed'] for item in result['checks'].values())
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
