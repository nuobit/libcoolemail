from distutils.core import setup

setup(name='libcoolemail',
      version='v0.1.0',
      author="NuoBiT Solutions, S.L., Eric Antones",
      author_email='eantones@nuobit.com',
      package_dir={'libcoolemail': 'src'},
      packages=['libcoolemail'],
      install_requires=[
          'pyOpenSSL',
      ],

      url='https://github.com/nuobit/libcoolemail',
      keywords=['email', 'handler', 'logging', 'smtp'],
      license='AGPLv3+',
      platform='Linux',
      description='SMTP utils',
      long_description='SMTP send email, log handler',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Email'
      ]
)
