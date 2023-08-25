auta_backend | The above exception was the direct cause of the following exception:
auta_backend | 
auta_backend | Traceback (most recent call last):
auta_backend |   File "/usr/local/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
auta_backend |     self.run()
auta_backend |   File "/usr/local/lib/python3.10/multiprocessing/process.py", line 108, in run
auta_backend |     self._target(*self._args, **self._kwargs)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/uvicorn/_subprocess.py", line 76, in subprocess_started
auta_backend |     target(sockets=sockets)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/uvicorn/server.py", line 61, in run
auta_backend |     return asyncio.run(self.serve(sockets=sockets))
auta_backend |   File "/usr/local/lib/python3.10/asyncio/runners.py", line 44, in run
auta_backend |     return loop.run_until_complete(main)
auta_backend |   File "/usr/local/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
auta_backend |     return future.result()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/uvicorn/server.py", line 68, in serve
auta_backend |     config.load()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/uvicorn/config.py", line 467, in load
auta_backend |     self.loaded_app = import_from_string(self.app)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/uvicorn/importer.py", line 21, in import_from_string
auta_backend |     module = importlib.import_module(module_str)
auta_backend |   File "/usr/local/lib/python3.10/importlib/__init__.py", line 126, in import_module
auta_backend |     return _bootstrap._gcd_import(name[level:], package, level)
auta_backend |   File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
auta_backend |   File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
auta_backend |   File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
auta_backend |   File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
auta_backend |   File "<frozen importlib._bootstrap_external>", line 883, in exec_module
auta_backend |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
auta_backend |   File "/app/server.py", line 74, in <module>
auta_backend |     models.Base.metadata.create_all(engine)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/sql/schema.py", line 5792, in create_all
auta_backend |     bind._run_ddl_visitor(
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3238, in _run_ddl_visitor
auta_backend |     with self.begin() as conn:
auta_backend |   File "/usr/local/lib/python3.10/contextlib.py", line 135, in __enter__
auta_backend |     return next(self.gen)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3228, in begin
auta_backend |     with self.connect() as conn:
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3264, in connect
auta_backend |     return self._connection_cls(self)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 147, in __init__
auta_backend |     Connection._handle_dbapi_exception_noconnection(
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 2426, in _handle_dbapi_exception_noconnection
auta_backend |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
auta_backend |     self._dbapi_connection = engine.raw_connection()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/base.py", line 3288, in raw_connection
auta_backend |     return self.pool.connect()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 452, in connect
auta_backend |     return _ConnectionFairy._checkout(self)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 1267, in _checkout
auta_backend |     fairy = _ConnectionRecord.checkout(pool)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 716, in checkout
auta_backend |     rec = pool._do_get()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 169, in _do_get
auta_backend |     with util.safe_reraise():
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
auta_backend |     raise exc_value.with_traceback(exc_tb)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/impl.py", line 167, in _do_get
auta_backend |     return self._create_connection()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 393, in _create_connection
auta_backend |     return _ConnectionRecord(self)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 678, in __init__
auta_backend |     self.__connect()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 902, in __connect
auta_backend |     with util.safe_reraise():
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/util/langhelpers.py", line 147, in __exit__
auta_backend |     raise exc_value.with_traceback(exc_tb)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/pool/base.py", line 898, in __connect
auta_backend |     self.dbapi_connection = connection = pool._invoke_creator(self)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/create.py", line 637, in connect
auta_backend |     return dialect.connect(*cargs, **cparams)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/sqlalchemy/engine/default.py", line 615, in connect
auta_backend |     return self.loaded_dbapi.connect(*cargs, **cparams)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/mysql/connector/pooling.py", line 293, in connect
auta_backend |     return CMySQLConnection(*args, **kwargs)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/mysql/connector/connection_cext.py", line 120, in __init__
auta_backend |     self.connect(**kwargs)
auta_backend |   File "/usr/local/lib/python3.10/site-packages/mysql/connector/abstracts.py", line 1181, in connect
auta_backend |     self._open_connection()
auta_backend |   File "/usr/local/lib/python3.10/site-packages/mysql/connector/connection_cext.py", line 296, in _open_connection
auta_backend |     raise get_mysql_exception(
auta_backend | sqlalchemy.exc.DatabaseError: (mysql.connector.errors.DatabaseError) 2003 (HY000): Can't connect to MySQL server on 'mariadb:3306' (111)
auta_backend | (Background on this error at: https://sqlalche.me/e/20/4xp6)