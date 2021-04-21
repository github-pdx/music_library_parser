from setuptools import setup

setup(
    name='music_library_parser',
    version='1.5.0',
    packages=['media_parser', 'media_parser.db',
              'media_parser.lib', 'tests'],
    url='https://github.com/averille-dev/music_library_parser',
    license='MIT',
    author='averille-dev',
    author_email='software.pdx@protonmail.com',
    description=f'extract metadata from ['.mp3','.m4a','.flac','.wma'] files'
)
