# npg-tracking-python
This package contains an ORM for an existing database schema, which hosts information about sequencing runs. A Perl ORM for the same schema is defined in [npg_tracking](https://github.com/wtsi-npg/npg_tracking). Migrations for that schema are also tracked in the Perl package.

This package was tested for read-only operations. Business logic for `create` and `update` operation for different database tables is implemented in the Perl package. We advise against performing `write` operations using this ORM.

This ORM has been auto-generated with [`sqlacodegen 3.1.1`](https://pypi.org/project/sqlacodegen/3.1.1/) 
```
sqlacodegen --generator declarative mysql+pymysql://user:pass@host:port/dbname > src/npgtracking/db/schema.py
```
The package also contains utility functions for data retrieval.

## Development

```
pip install .[test]
pytest
```
