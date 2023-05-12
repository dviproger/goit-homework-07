from setuptools import setup, find_namespace_packages

setup(
    name='Clean_folder',
    version='0.0.1',
    description='Program sorter',
    url='https://github.com/dviproger/goit-homework-06.git',
    author='DVIProger',
    author_email='DVIProger@gmail.com',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3'],
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:main']}
)
