try:
    from d51.django.virtualenv.test_runner import run_tests
except ImportError:
    print "Please install d51.django.virtualenv.test_runner to run these tests"

def main():
    settings = {
        "INSTALLED_APPS": (
            "django.contrib.contenttypes",
            "d51.django.apps.regions",
        ),
        'DATABASE_ENGINE': 'postgresql_psycopg2',
        'DATABASE_NAME': 'd51_django_apps_regions',
        'TEST_RUNNER': 'django.contrib.gis.tests.run_tests',
    }
    run_tests(settings, 'regions')

if __name__ == '__main__':
    main()
