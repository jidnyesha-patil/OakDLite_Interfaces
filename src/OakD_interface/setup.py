from setuptools import setup

package_name = 'OakD_interface'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rushi',
    maintainer_email='rdeshmukh@wpi.edu',
    description='TODO: Package description',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'Image_Publisher = OakD_interface.getFrames:main',
            'Image_Subscriber = OakD_interface.showFrames:main',
        ],
    },
)
