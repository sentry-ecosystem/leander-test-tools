from concurrent.futures import ThreadPoolExecutor, TimeoutError
from time import sleep


def deliver_message() -> dict:
    def wait_for_hallway_clearance() -> str:
        sleep(0.05)
        return "delivered"

    with ThreadPoolExecutor(max_workers=1) as executor:
        delivery = executor.submit(wait_for_hallway_clearance)
        try:
            status = delivery.result(timeout=0.001)
        except TimeoutError as error:
            raise TimeoutError("O&D message timed out awaiting Milchick approval") from error
    return {"status": status}
