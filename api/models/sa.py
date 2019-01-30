from flask_sqlalchemy import (SessionBase, SignallingSession, SQLAlchemy,
                              get_state, orm)


class CustomSQLAlchemy(SQLAlchemy):
    """Re-write some methods to avoid deprecation warnings.
    """

    def apply_driver_hacks(self, app, info, options):
        """SQLAlchemy now gives SADeprecationWarnings for the "convert_unicode"
        parameter that Flask-SQLAlchemy injects. We avoid the warnings by not
        passing that parameter.
        """
        if "convert_unicode" in options:
            del options["convert_unicode"]
        super().apply_driver_hacks(app, info, options)

    def create_session(self, options):
        """Create the session factory used by :meth:`create_scoped_session`.
        The factory **must** return an object that SQLAlchemy recognizes as a session,
        or registering session events may raise an exception.
        Valid factories include a :class:`~sqlalchemy.orm.session.Session`
        class or a :class:`~sqlalchemy.orm.session.sessionmaker`.
        The default implementation creates a ``sessionmaker``
        for :class:`SignallingSession`.
        :param options: dict of keyword arguments passed to session class
        """
        return orm.sessionmaker(class_=CustomSignallingSession, db=self, **options)


class CustomSignallingSession(SignallingSession):
    def get_bind(self, mapper=None, clause=None):
        # mapper is None if someone tries to just get a connection
        if mapper is not None:
            info = getattr(mapper.persist_selectable, "info", {})
            bind_key = info.get("bind_key")
            if bind_key is not None:
                state = get_state(self.app)
                return state.db.get_engine(self.app, bind=bind_key)
        return SessionBase.get_bind(self, mapper, clause)
