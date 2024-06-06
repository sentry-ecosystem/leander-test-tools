import argparse
from datetime import datetime

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

LOCAL_SENTRY_DSN = "https://69b42e5ad1606cdf535262d253800f93@leeandher.ngrok.io/2"
LOCAL_GETSENTRY_DSN = (
    "https://287a7215db7931a63e5d7a2f62506f9a@leeandher.ngrok.io/4506974030528528"
)
# acme-e0 // leander-test-flask
HOSTED_DSN = "https://f61444722ce0460892f94a6d5d110596@o951660.ingest.sentry.io/5900755"
SILO_DSN = "https://e9a3d278c7729cdf4e9d2162ba377d83@test-region.test.my.sentry.io/4505992947957808"

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument(
    "instance",
    default="sentry",
    const="sentry",
    nargs="?",
    choices=["sentry", "getsentry", "hosted", "silo"],
    help="Sentry instance to receive errors",
)


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == "getsentry":
        return LOCAL_GETSENTRY_DSN
    elif args.instance == "hosted":
        return HOSTED_DSN
    elif args.instance == "silo":
        return SILO_DSN
    else:
        return LOCAL_SENTRY_DSN


sentry_sdk.init(
    dsn=dsn_selector(),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    release="abcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyzabcdefghijklmnoqrstuvwxyz",
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello World!</h1>"


@app.route("/error")
def error():
    sentry_sdk.set_user(
        {
            "id": 12,
            "email": "leander.rodrigues@sentry.io",
            "username": "leeandher",
            "ip_address": "12.34.56.78",
            "other": "property",
            "location": "canada",
            "data": [1, 2, 3, 4],
        }
    )
    sentry_sdk.set_tag("my_favourite.color", "teal")
    sentry_sdk.set_tag("my_favourite.food", "sushi")
    sentry_sdk.set_tag("my_favourite.car", "train")
    sentry_sdk.set_tag("super", "text")
    sentry_sdk.set_tag("api_key", "12341234")
    sentry_sdk.set_tag("CLIENT_SECRET", "b12")
    sentry_sdk.set_tag(
        "extra-long",
        "veryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryverylong",
    )
    # sentry_sdk.set_tag(
    #     "invalid-char",
    #     """invale\n\ncharacters
    #     🇨🇦🔥🤡
    #     """,
    # )
    sentry_sdk.set_tag("slash/1", "some-value")
    sentry_sdk.set_tag("super.nested.value1", "text1")
    sentry_sdk.set_tag("far.too.many.nested.tags.to.be.valuable", "some value")
    sentry_sdk.set_tag("super.nested.value2", "text2")
    sentry_sdk.set_tag("super.nested.value3", "text3")
    sentry_sdk.set_tag("super.nested2.value4", "text4")
    sentry_sdk.set_tag("magic.nested2.again.value1", "text1")
    sentry_sdk.set_tag("magic.nested3.again.value2", "text2")
    sentry_sdk.set_tag("magic.nested.again.value3", "text3")
    sentry_sdk.set_tag("magic.nested3.again.value4", "text4")
    sentry_sdk.set_tag(
        "magic.nested.again.value5", "verylongtextthatcouldevenbealinkorsomething"
    )
    sentry_sdk.set_tag("double..dot", "display these normally")
    sentry_sdk.set_tag(
        "triple...dot", "this is a very long tag its probably a bit too long actually"
    )
    sentry_sdk.set_context(
        "secrets",
        {
            "api_key": "mysupersecretapikey",
            "CLIENT_SECRET": "mysupersecretclientsecret",
            "another valid key": "my valid value",
        },
    )
    sentry_sdk.set_context(
        "laravel",
        {
            "constructor": "some value",
            "state-value": "something-phpy",
            "context-key": "another-value",
            "my number": 123123,
        },
    )
    sentry_sdk.set_context(
        "another_try",
        {
            "drink": "coffee",
            "music": "loud",
            "wallet": "empty",
            "some_url": "http://www.reallylong.link/rll/k7/A8cg6cTe4tHP6yerlsKjKhfvE5CtFa6FetaoNzjV10AsILYF4tZc5npIYtue/8XqrFH49ue1ukwfweG8iaTFMx0UFJsf5o1QQDRQj_ltJyYTAXhZARQxIuQtidkk0aM_CaBrJf/3ZfJ0Xx5z8wx8KPjKL/ZyHpbOxsfAF3aODxqTLzLjNHajdEcqCV1OT_ITYgF2dyCys6RFhr5Ipl7ZHiG6henfl98CwL7gq56ihxzDWR03yQbue_XRt7wal_mdeZOxNDStI8Fun1/X3Pac7J3fAks8FQP2_HAw0XKUCDrc6v3AwcujePEGyqKHt3nUSCUuPaQAMA1qzOMTdyOFnif6zMlirEATBaajwZRKngIt6jeoRIYxidKUCYmlj14K/KNxzhoszqplL1hqn5BFd/HGlGE4f09jfUJWiS246ur8A4DM8cMOQ5j9lnQDOdQViKgYDMGftmb2XLymgHNfVNbMFMTADS85c_rYPf9mL3sVMBeFVGsq/2t9YlFBDHYJObEIXC4oRqkgFlY69ghDpd5kRojm1jgh2NB/r0BHPOVB5pEfJ9w6GWAO8UZTtYFOhHZDopX/MQMEJHnOaT6Er24BUF/vrvfqBQTDzgYZJZAb5shKExG51qZ9iBGmHEuarNrywLVab095mTIt7HkrlLvHlgWZIBHEDFsXVWQhvuoVcxvKvU3vL32aSizfnO7Hiw1GWycJxHBRgc4nx8kypUn5qRrBlhCq3BHMI6LkTSAywcLddDBUk2oHptVxBzM3EcPedwaKQiz3wIIbn1cCeeaZypvLk_2Wd8f0cX7nUoLD9kyINNPsqgvxEXgfw0qm3oyimrKHDU1LIO6yL9tw8cuUoltWmMvV29RtU9yFckWoTZexXeoUhkTubUIRD5YvzizgXa7YyzTSkG6Lm_Uszu3bZKeUdCpz9JSJYcjA/1HR0l4uC/zTS88CELdYYfzXUZkVg46aCHYFPxABilOUvci7Fwj94FCrmox6utl_ph51WF9GIhqSClp5CY1X8qAJj70fhJC/uju4BJ9OSCqHpgrOu6QJjrUDLRnWKOvvOn8nwMnqFgni/CjtB8rv0SoQGSzBEK7hDC0fJWr82IN1eC9hjJ8cODVTLV7wikXG5nfgNKhR5JKhRN3WrX2Xe/8_IEtc1MdoEJmoJdOY/4bzHnLFbDfQHqodKV51QBGPey2RFltiRdPWkgj0fz2Ka/_PXO0A4teHK7ZD_oHA2zTh/bgg_LWLyBjQGucPwF40ZrG/ulwkExB8GFAtAYDADLm_OTsS1PQU62I2Bb5ro8ZBSn5K8sMKMeysZsvlL4sUc3nwDbCPUO7dbzibM51DIzkSl5YWz4JTpwCQSPFcSpnXvchY5NZ4cAbAGVnXHUN3uIyGo0sbxrr6Lz45L1k5rzjbL/XqPyREdo2nq2NC7OKh5OvlM7ULkuvR9fefIJr1rULtjttq13xOguhgk3MSzcV9VY9QWy8OhCn27Tjv9fcjYP9yc8tytiApq38E33ARZq1gzVdVzBYU5PA9/UFe9K9JxdG6ZTnQnlCEq7dNHAOl/0XvyByMw0YAlMGPjB_/y8pUk_LofcMxVBmzVJ98HOI7XvJrtCnVgnh60ASc5HMH3HNc2POCaVDpzAPSjINlRBLt62lubg9SyABUmZ3n0CKEk7TEu23Sg5/y3si2nx6ZSBOcGWwXyhf_tCHZCG64aToPYsLCfJm1vFf00nPQVPUPXDfy0uDnELFOdBcCqPFqSV6ZnPFhZARa8K6F9Zj8Kj7LlByl8aAVXhE0n6Soo977MrUzC5VacgYETFhGmd9M0ERxEBggUsdTfiDhyujQNuGzwYX3UmvfjiGseuZu7cr4mHEEOSgn4vl9L9QhvLeWuYdvpfP0fQI9iDTyw46pwZ3OUwxpdWXjqaGrbDraQb/VHvC1MyX4O6gEn8RnkD3wB2j3sJLtmgz3Gsk3yiDG7o4x",
            "some_longer_url": "http://www.reallylong.link/rll/k7/A8cg6cTe4tHP6yerlsKjKhfvE5CtFa6FetaoNzjV10AsILYF4tZc5npIYtue/8XqrFH49ue1ukwfweG8iaTFMx0UFJsf5o1QQDRQj_ltJyYTAXhZARQxIuQtidkk0aM_CaBrJf/3ZfJ0Xx5z8wx8KPjKL/ZyHpbOxsfAF3aODxqTLzLjNHajdEcqCV1OT_ITYgF2dyCys6RFhr5Ipl7ZHiG6henfl98CwL7gq56ihxzDWR03yQbue_XRt7wal_mdeZOxNDStI8Fun1/X3Pac7J3fAks8FQP2_HAw0XKUCDrc6v3AwcujePEGyqKHt3nUSCUuPaQAMA1qzOMTdyOFnif6zMlirEATBaajwZRKngIt6jeoRIYxidKUCYmlj14K/KNxzhoszqplL1hqn5BFd/HGlGE4f09jfUJWiS246ur8A4DM8cMOQ5j9lnQDOdQViKgYDMGftmb2XLymgHNfVNbMFMTADS85c_rYPf9mL3sVMBeFVGsq/2t9YlFBDHYJObEIXC4oRqkgFlY69ghDpd5kRojm1jgh2NB/r0BHPOVB5pEfJ9w6GWAO8UZTtYFOhHZDopX/MQMEJHnOaT6Er24BUF/vrvfqBQTDzgYZJZAb5shKExG51qZ9iBGmHEuarNrywLVab095mTIt7HkrlLvHlgWZIBHEDFsXVWQhvuoVcxvKvU3vL32aSizfnO7Hiw1GWycJxHBRgc4nx8kypUn5qRrBlhCq3BHMI6LkTSAywcLddDBUk2oHptVxBzM3EcPedwaKQiz3wIIbn1cCeeaZypvLk_2Wd8f0cX7nUoLD9kyINNPsqgvxEXgfw0qm3oyimrKHDU1LIO6yL9tw8cuUoltWmMvV29RtU9yFckWoTZexXeoUhkTubUIRD5YvzizgXa7YyzTSkG6Lm_Uszu3bZKeUdCpz9JSJYcjA/1HR0l4uC/zTS88CELdYYfzXUZkVg46aCHYFPxABilOUvci7Fwj94FCrmox6utl_ph51WF9GIhqSClp5CY1X8qAJj70fhJC/uju4BJ9OSCqHpgrOu6QJjrUDLRnWKOvvOn8nwMnqFgni/CjtB8rv0SoQGSzBEK7hDC0fJWr82IN1eC9hjJ8cODVTLV7wikXG5nfgNKhR5JKhRN3WrX2Xe/8_IEtc1MdoEJmoJdOY/4bzHnLFbDfQHqodKV51QBGPey2RFltiRdPWkgj0fz2Ka/_PXO0A4teHK7ZD_oHA2zTh/bgg_LWLyBjQGucPwF40ZrG/ulwkExB8GFAtAYDADLm_OTsS1PQU62I2Bb5ro8ZBSn5K8sMKMeysZsvlL4sUc3nwDbCPUO7dbzibM51DIzkSl5YWz4JTpwCQSPFcSpnXvchY5NZ4cAbAGVnXHUN3uIyGo0sbxrr6Lz45L1k5rzjbL/XqPyREdo2nq2NC7OKh5OvlM7ULkuvR9fefIJr1rULtjttq13xOguhgk3MSzcV9VY9QWy8OhCn27Tjv9fcjYP9yc8tytiApq38E33ARZq1gzVdVzBYU5PA9/UFe9K9JxdG6ZTnQnlCEq7dNHAOl/0XvyByMw0YAlMGPjB_/y8pUk_LofcMxVBmzVJ98HOI7XvJrtCnVgnh60ASc5HMH3HNc2POCaVDpzAPSjINlRBLt62lubg9SyABUmZ3n0CKEk7TEu23Sg5/y3si2nx6ZSBOcGWwXyhf_tCHZCG64aToPYsLCfJm1vFf00nPQVPUPXDfy0uDnELFOdBcCqPFqSV6ZnPFhZARa8K6F9Zj8Kj7LlByl8aAVXhE0n6Soo977MrUzC5VacgYETFhGmd9M0ERxEBggUsdTfiDhyujQNuGzwYX3UmvfjiGseuZu7cr4mHEEOSgn4vl9L9QhvLeWuYdvpfP0fQI9iDTyw46pwZ3OUwxpdWXjqaGrbDraQb/VHvC1MyX4O6gEn8RnkD3wB2j3sJLtmgz3Gsk3yiDG7o4x&referrer=http://www.reallylong.link/rll/k7/A8cg6cTe4tHP6yerlsKjKhfvE5CtFa6FetaoNzjV10AsILYF4tZc5npIYtue/8XqrFH49ue1ukwfweG8iaTFMx0UFJsf5o1QQDRQj_ltJyYTAXhZARQxIuQtidkk0aM_CaBrJf/3ZfJ0Xx5z8wx8KPjKL/ZyHpbOxsfAF3aODxqTLzLjNHajdEcqCV1OT_ITYgF2dyCys6RFhr5Ipl7ZHiG6henfl98CwL7gq56ihxzDWR03yQbue_XRt7wal_mdeZOxNDStI8Fun1/X3Pac7J3fAks8FQP2_HAw0XKUCDrc6v3AwcujePEGyqKHt3nUSCUuPaQAMA1qzOMTdyOFnif6zMlirEATBaajwZRKngIt6jeoRIYxidKUCYmlj14K/KNxzhoszqplL1hqn5BFd/HGlGE4f09jfUJWiS246ur8A4DM8cMOQ5j9lnQDOdQViKgYDMGftmb2XLymgHNfVNbMFMTADS85c_rYPf9mL3sVMBeFVGsq/2t9YlFBDHYJObEIXC4oRqkgFlY69ghDpd5kRojm1jgh2NB/r0BHPOVB5pEfJ9w6GWAO8UZTtYFOhHZDopX/MQMEJHnOaT6Er24BUF/vrvfqBQTDzgYZJZAb5shKExG51qZ9iBGmHEuarNrywLVab095mTIt7HkrlLvHlgWZIBHEDFsXVWQhvuoVcxvKvU3vL32aSizfnO7Hiw1GWycJxHBRgc4nx8kypUn5qRrBlhCq3BHMI6LkTSAywcLddDBUk2oHptVxBzM3EcPedwaKQiz3wIIbn1cCeeaZypvLk_2Wd8f0cX7nUoLD9kyINNPsqgvxEXgfw0qm3oyimrKHDU1LIO6yL9tw8cuUoltWmMvV29RtU9yFckWoTZexXeoUhkTubUIRD5YvzizgXa7YyzTSkG6Lm_Uszu3bZKeUdCpz9JSJYcjA/1HR0l4uC/zTS88CELdYYfzXUZkVg46aCHYFPxABilOUvci7Fwj94FCrmox6utl_ph51WF9GIhqSClp5CY1X8qAJj70fhJC/uju4BJ9OSCqHpgrOu6QJjrUDLRnWKOvvOn8nwMnqFgni/CjtB8rv0SoQGSzBEK7hDC0fJWr82IN1eC9hjJ8cODVTLV7wikXG5nfgNKhR5JKhRN3WrX2Xe/8_IEtc1MdoEJmoJdOY/4bzHnLFbDfQHqodKV51QBGPey2RFltiRdPWkgj0fz2Ka/_PXO0A4teHK7ZD_oHA2zTh/bgg_LWLyBjQGucPwF40ZrG/ulwkExB8GFAtAYDADLm_OTsS1PQU62I2Bb5ro8ZBSn5K8sMKMeysZsvlL4sUc3nwDbCPUO7dbzibM51DIzkSl5YWz4JTpwCQSPFcSpnXvchY5NZ4cAbAGVnXHUN3uIyGo0sbxrr6Lz45L1k5rzjbL/XqPyREdo2nq2NC7OKh5OvlM7ULkuvR9fefIJr1rULtjttq13xOguhgk3MSzcV9VY9QWy8OhCn27Tjv9fcjYP9yc8tytiApq38E33ARZq1gzVdVzBYU5PA9/UFe9K9JxdG6ZTnQnlCEq7dNHAOl/0XvyByMw0YAlMGPjB_/y8pUk_LofcMxVBmzVJ98HOI7XvJrtCnVgnh60ASc5HMH3HNc2POCaVDpzAPSjINlRBLt62lubg9SyABUmZ3n0CKEk7TEu23Sg5/y3si2nx6ZSBOcGWwXyhf_tCHZCG64aToPYsLCfJm1vFf00nPQVPUPXDfy0uDnELFOdBcCqPFqSV6ZnPFhZARa8K6F9Zj8Kj7LlByl8aAVXhE0n6Soo977MrUzC5VacgYETFhGmd9M0ERxEBggUsdTfiDhyujQNuGzwYX3UmvfjiGseuZu7cr4mHEEOSgn4vl9L9QhvLeWuYdvpfP0fQI9iDTyw46pwZ3OUwxpdWXjqaGrbDraQb/VHvC1MyX4O6gEn8RnkD3wB2j3sJLtmgz3Gsk3yiDG7o4x",
        },
    )
    sentry_sdk.set_context(
        "some new stuff",
        {
            "number": 1231,
            "array": [1, 2, 3],
            "date": datetime.now(),
            "dict": {
                "some": "key",
                "another": [{"key": "something else", "value": "another one"}],
            },
            "long_dict": {
                "prop0": 0,
                "prop1": 1,
                "prop2": 2,
                "prop3": 3,
                "prop4": 4,
                "prop5": 5,
                "prop6": 6,
                "prop7": 7,
                "prop8": 8,
                "prop9": 9,
                "prop10": 10,
                "prop11": 11,
                "prop12": 12,
                "prop13": 13,
                "prop14": 14,
                "prop15": 15,
                "prop16": 16,
                "prop17": 17,
                "prop18": 18,
                "prop19": 19,
                "prop20": 20,
                "prop21": 21,
                "prop22": 22,
                "prop23": 23,
                "prop24": 24,
                "prop25": 25,
                "prop26": 26,
                "prop27": 27,
                "prop28": 28,
                "prop29": 29,
            },
            "long_arr": [
                "prop_ 0",
                "prop_ 1",
                "prop_ 2",
                "prop_ 3",
                "prop_ 4",
                "prop_ 5",
                "prop_ 6",
                "prop_ 7",
                "prop_ 8",
                "prop_ 9",
                "prop10_10",
                "prop11_11",
                "prop12_12",
                "prop13_13",
                "prop14_14",
                "prop15_15",
                "prop16_16",
                "prop17_17",
                "prop18_18",
                "prop19_19",
                "prop20_20",
                "prop21_21",
                "prop22_22",
                "prop23_23",
                "prop24_24",
                "prop25_25",
                "prop26_26",
                "prop27_27",
                "prop28_28",
                "prop29_29",
            ],
            "string": "this is a a very long string",
        },
    )

    # sentry_sdk.set_context(
    #     "browser",
    #     {
    #         "attempting": "override",
    #         "name": "Chrome",
    #         "version": "1.2.3",
    #         "api_key": "mysupersecretapikey",
    #         "CLIENT_SECRET": "mysupersecretclientsecret",
    #         "fav-browser": "opera",
    #     },
    # )
    sentry_sdk.set_context(
        "trace",
        {
            "attempting": "override",
            "name": "Chrome",
            "status": "elementary",
            "Trace ID": "9258ee02268dbd01",
            "api_key": "mysupersecretapikey",
            "CLIENT_SECRET": "mysupersecretclientsecret",
            "fav-browser": "opera",
        },
    )
    sentry_sdk.set_context(
        "scrubthis",
        {
            "some value": {
                "nested": ["okay1", "okay2"],
                "tree": {
                    "api_key": "mysupersecretapikey",
                    "CLIENT_SECRET": "mysupersecretclientsecret",
                },
            }
        },
    )

    sentry_sdk.set_context("replay", {"replay_id": "61d2d7c5acf448ffa8e2f8f973e2cd36"})
    sentry_sdk.set_tag("bigNumber", 608548899684111178)
    with sentry_sdk.configure_scope() as scope:
        scope.set_context(
            "large_numbers",
            {
                "decimal_number": 123456.789,
                "number": 123456789,
                "negative_number": -123456789,
                "big_decimal_number": 123456789.123456789,
                "big_number": 123456789123456789,
                "big_negative_number": -123456789123456789,
                "bug_report_number": 608548899684111178,
            },
        )
        from src.runner import error_function

        print(name122)
        error_function()


@app.route("/txn")
def transaction():
    counter = 1
    with sentry_sdk.start_transaction(op="task", name="Test TXN"):
        with sentry_sdk.start_span(description="Test Span"):
            while counter < 10000:
                counter = counter + 1
        return "<h1>Test</h1>"


if __name__ == "__main__":
    app.run(debug=True)
