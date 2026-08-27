from concurrent.futures import ThreadPoolExecutor, TimeoutError
from time import sleep

MESSAGE_DELIVERY_TIMEOUT_SECONDS = 30.0


def deliver_message() -> dict:
    def wait_for_hallway_clearance() -> str:
        sleep(0.05)
        return "delivered"

    with ThreadPoolExecutor(max_workers=1) as executor:
        delivery = executor.submit(wait_for_hallway_clearance)
        try:
            status = delivery.result(timeout=MESSAGE_DELIVERY_TIMEOUT_SECONDS)
        except TimeoutError as error:
            raise TimeoutError("O&D message timed out awaiting Milchick approval") from error
    return {"status": status}
