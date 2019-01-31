__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'


class HealthsiteRouter(object):
    docker_osm_apps = ['localities_osm']

    def db_for_read(self, model, **hints):
        database = getattr(model, '_DATABASE', None)
        if database:
            return database
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        database = getattr(model, '_DATABASE', None)
        if database:
            return database
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        db_list = ('default',)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure all qgis app is allowed if db is qgis
        """
        if app_label in self.docker_osm_apps:
            return db == 'docker_osm'
        return db == 'default'
