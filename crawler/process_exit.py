import os
import signal
import multiprocessing


class GracefulExitException(Exception):
    @staticmethod
    def sigterm_handler(signum, frame):
        raise GracefulExitException()

    pass


class GracefulExitEvent(object):
    def __init__(self):
        self.workers = []
        self.exit_event = multiprocessing.Event()

        # Use signal handler to throw exception which can be caught
        # by worker process to allow graceful exit.
        signal.signal(signal.SIGTERM, GracefulExitException.sigterm_handler)
        pass

    def reg_worker(self, wp):
        self.workers.append(wp)
        pass

    def is_stop(self):
        return self.exit_event.is_set()

    def notify_stop(self):
        self.exit_event.set()

    def wait_all(self):
        while True:
            try:
                for wp in self.workers:
                    wp.join()

                print( "main process(%d) exit." % os.getpid())
                break
            except GracefulExitException:
                self.notify_stop()
                print("main process(%d) got GracefulExitException." % os.getpid())
            except Exception as ex:
                self.notify_stop()
                print("main process(%d) got unexpected Exception: %r" % (os.getpid(), ex))
                break
        pass

    #######################################################################


def worker_proc(gee):
    import sys, time
    print("worker(%d) start ..." % os.getpid())
    try:
        while not gee.is_stop():
            # do task job here
            print(".",)
            time.sleep(10)
        else:
            print("")
            print("worker process(%d) got exit event." % os.getpid())
            print("worker process(%d) do cleanup..." % os.getpid())
            time.sleep(1)
            print("[%d] 3" % os.getpid())
            time.sleep(1)
            print("[%d] 2" % os.getpid())
            time.sleep(1)
            print("[%d] 1" % os.getpid())

    except GracefulExitException:
        print("worker(%d) got GracefulExitException" % os.getpid())
    except Exception as ex:
        print("Exception:", ex)
    except KeyboardInterrupt as e:
        print("!@@@")
    finally:
        print("worker(%d) exit." % os.getpid())
        sys.exit(0)


if __name__ == "__main__":
    import sys

    print("main process(%d) start" % os.getpid())

    gee = GracefulExitEvent()

    # Start some workers process and run forever
    for i in range(0, 10):
        wp = multiprocessing.Process(target=worker_proc, args=(gee,))
        wp.start()
        gee.reg_worker(wp)

    gee.wait_all()
    sys.exit(0)