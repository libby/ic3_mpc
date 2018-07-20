from setuptools import setup


dev_require = [
    'ipdb',
    'ipython',
]

setup(
    name='mpc',
    version='0.0.1',
    py_modules=['number_shoot_out'],
    extras_require={'dev': dev_require},
)
