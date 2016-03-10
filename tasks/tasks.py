from paver.easy import task, sh, call_task


@task
def run_server():
    sh('python3 feature_rerporter.py')


@task
def test_and_code_style():
    call_task('flake8')
    call_task('unit_test')


@task
def unit_test():
    sh('nosetests')


@task
def flake8():
    sh('flake8')
