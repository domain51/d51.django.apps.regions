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
    }
    run_tests(settings, 'regions')

if __name__ == '__main__':
    main()
