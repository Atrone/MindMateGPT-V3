import asyncio
import os
import unittest
from unittest import skip

import openai

from backend.base.free.service import FreeAppService

openai.api_key = os.getenv("apikey")


class TestInteractiveScenario(unittest.TestCase):
    def setUp(self):
        self.openai = openai  # Replace 'YourApiKey' with your actual API key
        self.instance = FreeAppService(self.openai, None, os.getenv(
            "INITIAL_PROMPT"))  # Replace YourClassNameHere with your actual class name

    @skip
    def test_chat_free_form(self):
        user_data = {"first_name": "Bill", 'childhood': "great", "relationship": "in a relationship", "mbti": "ENTJ",
                     "growup": "America", "live": "America",
                     "criminal": "nope", "drugs": "nope", "family": "great", "religion": "Catholic",
                     "education": "University", "medication": "None", "working": "yes, mailman"}
        loop = asyncio.get_event_loop()
        prompt = os.getenv(
            "INITIAL_PROMPT") + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"


    def test_chat_ENTJ_America_Catholic_relationship_university_mailman_sober_no_criminal_happy(self):
        user_data = {"first_name": "Bill", 'childhood': "great", "relationship": "in a relationship", "mbti": "ENTJ",
                     "growup": "America", "live": "America",
                     "criminal": "nope", "drugs": "nope", "family": "great", "religion": "Catholic",
                     "education": "University", "medication": "None", "working": "yes, mailman"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            print(openai.Moderation.create(prompt))
            response = loop.run_until_complete(self.instance.generate_response(prompt))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"
    @skip
    def test_chat_INFJ_America_Catholic_relationship_university_mailman_sober_no_criminal_happy(self):
        user_data = {"first_name": "Billy", 'childhood': "great", "relationship": "in a relationship", "mbti": "INFJ",
                     "growup": "America", "live": "America",
                     "criminal": "nope", "drugs": "nope", "family": "great", "religion": "Catholic",
                     "education": "University", "medication": "None", "working": "yes, mailman"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt, {"status": "success"}))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"


    @skip
    def test_chat_ENTP_Canada_Atheist_no_relationship_Highschool_unemployed_alcohol_criminal_sad_xanax(self):
        user_data = {"first_name": "Jim", 'childhood': "really bad, i never felt like i belonged",
                     "relationship": "nonexistent", "mbti": "ENTP", "growup": "Canada", "live": "Canada",
                     "criminal": "just drug stuff", "drugs": "alcoholic", "family": "they never accepted me",
                     "religion": "atheist", "education": "Highschool", "medication": "Xanax", "working": "no"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt, {"status": "success"}))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_INTP_Canada_Atheist_no_relationship_Highschool_goodJob_alcohol_noCriminal_sad_xanax(self):
        user_data = {"first_name": "Aaron", 'childhood': "really bad, i never felt like i belonged",
                     "relationship": "nonexistent", "mbti": "INTP", "growup": "Canada", "live": "Canada",
                     "criminal": "None", "drugs": "alcoholic", "family": "they never accepted me",
                     "religion": "atheist", "education": "Highschool", "medication": "Xanax", "working": "yes, as a principal software engineer"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt, {"status": "success"}))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_ENFP_China_Catholic_relationship_university_mailman_sober_no_criminal_happy(self):
        user_data = {"first_name": "James", 'childhood': "great", "relationship": "in a relationship", "mbti": "ENFP",
                     "growup": "China", "live": "China",
                     "criminal": "nope", "drugs": "nope", "family": "great", "religion": "Catholic",
                     "education": "University", "medication": "None", "working": "no"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt, {"status": "success"}))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_ISTP_China_Catholic_relationship_university_mailman_sober_no_criminal_happy(self):
        user_data = {"first_name": "Kenny", 'childhood': "great", "relationship": "in a relationship", "mbti": "ISTP",
                     "growup": "China", "live": "China",
                     "criminal": "nope", "drugs": "terrible alcoholic", "family": "great", "religion": "Catholic",
                     "education": "University", "medication": "None", "working": "yes"}
        loop = asyncio.get_event_loop()
        prompt = loop.run_until_complete(self.instance.format_prompt(user_data)) + "Hey" + "\n\n\n\n  "
        while True:
            response = loop.run_until_complete(self.instance.generate_response(prompt, {"status": "success"}))
            print(response)
            prompt += "\n\n\n\n" + response + "\n\n\n\n"
            prompt += "\n\n\n\n" + input() + "\n\n\n\n"
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"


if __name__ == '__main__':
    unittest.main()
