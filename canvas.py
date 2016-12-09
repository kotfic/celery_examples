from fib import app
from fib.tasks import add, mul, xsum

if __name__ == "__main__":

    # NB: All examples taken from celery Canvas Docs
    # http://docs.celeryproject.org/en/latest/userguide/canvas.html

    ###
    # Celery APIs
    #

    # A normal function call
    a = add(5, 5)

    # Highest level API for distributing a task
    a = add.delay(4, 4)

    print(a.result)

    # Signatures: One level deeper
    sig = add.s(3, 3)
    a = sig.delay()

    print(a.result)

    # One level deeper (apply_async kwargs give
    # you fine-grained control over task exectuion)
    # a = add.apply_async((2, 2), {"sleep": 1})

    # Lowest possible API
    # a = app.send_task("fib.tasks.add", (2, 2))


    ###
    # Partials
    #

    partial = add.s(4)
    a = partial.delay(4)

    print(a.result)

    ###
    # Chains
    #

    from celery import chain

    # 2 + 2 + 6 + 8
    c = chain(add.s(2, 2), add.s(6), add.s(8))
    a = c.delay()

    print(a.result)

    # Alternet syntax
    c = (add.s(2, 2) | add.s(6, sleep=3) | add.s(8))
    a = c.delay()

    print(a.result)

    ###
    # Groups
    #

    from celery import group

    g = group(add.s(i, i) for i in range(10))
    a = g.delay()

    print(a.join())

    ###
    # Chords
    #
    from celery import chord

    ch = chord((add.s(i, i) for i in range(10)), xsum.s())
    a = ch.delay()

    print(a.result)


    ###
    # Chord upgrades
    #

    # COMBO BONOUS!!
    c3 = (group(add.s(i, i) for i in range(10)) | xsum.s())
    a = c3.delay()

    print(a.result)

    ###
    # Chain Partials
    #

    # ((X + 4) * 8)
    c1 = (add.s(4) | mul.s(8))

    # (16 + 4) * 8)
    a = c1.delay(16)

    print(a.result)

    # Chain can be connected
    # ((4 + 16) * 2)
    c2 = (add.s(4, 16) | mul.s(2))

    # Bonkers
    # X = ((4 + 16) * 2)
    # (X + 4) * 8)
    c3 = (c2 | c1)
    a = c3.delay()

    print(a.result)

    ###
    # Slightly less Abstract
    #
    #  new_user_workflow = \
    #     (create_user.s() | group(import_contacts.s(), welcome_email.s()))
    #
    #  new_user_workflow.delay(
    #      username='artv',
    #      first='Art',
    #      last='Vandelay',
    #      email='art@vandelay.com')


    ###
    # What I wish I had known about for my Grad work
    #
    # from previous.literature import classifier, best_f1
    # from my.domain import param_sweep
    #
    # thesis = (group(classifier.s(p) for p in param_sweep()) | best_f1.s())
    # result = thesis.delay()  # <= funny because it is true
    #

    ###
    # Other Cool Stuff!
    #

    # Group API
    #  Check in on how many tasks are in what state
    #  (e.g. failed, waiting, ready, complete)

    # Chunks
    #  Can be used for scatter/gather paradigms

    # Intermediate Chain results

    # Error callbacks

    # Task Skewing

    print("Done!")
