from setuptools import setup, find_packages

version = "4.2.0a1"

setup(name='Products.MeetingCPASLalouviere',
      version=version,
      description=u"PloneMeeting profile for CPAS of La Louviere.",
      long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
      ],
      keywords="",
      author="Olivier Delaere",
      author_email="olivier.delaere@imio.be",
      url="http://www.imio.be/produits/gestion-des-deliberations",
      license="GPL",
      packages=find_packages("src"),
      package_dir={"": "src"},
      namespace_packages=["Products"],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(test=["Products.PloneMeeting[test]"], templates=["Genshi", ]),
      install_requires=[
          "setuptools",
          "Products.CMFPlone",
          "Pillow",
          "Products.PloneMeeting",
          "Products.MeetingCommunes",
      ],
      entry_points={},
      )
