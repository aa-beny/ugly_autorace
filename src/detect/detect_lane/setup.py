from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'detect_lane'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'), glob(os.path.join('launch','*launch.[pxy][yma]'))),
        (os.path.join('share',package_name,'config'), glob(os.path.join('config/*.yaml'))),
        (os.path.join('share',package_name,'config'), glob(os.path.join('config/*.rviz')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='anderson',
    maintainer_email='anderson@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'detect_lane = detect_lane.detect_lane:main',
            'hsv_param_adjustment = detect_lane.hsv_param_adjustment:main',
            'key_pub_signs = detect_lane.key_pub_signs:main',
            'recive_key_pub_signs = detect_lane.recive_key_pub_signs:main',
            'test_key_pub_signs = detect_lane.test_key_pub_signs:main',
        ],
    },
)
