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
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": os.getenv(
            "INITIAL_PROMPT")}, {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_ENTJ_relationship(self):  # PASSED
        # Use more feeling tone and empathy

        # I can understand why you might feel frustrated and upset in this situation. It's important to remember that
        # everyone has their own pace when it comes to defining relationships. Have you talked to your boyfriend
        # about your feelings and concerns? Communication is key in understanding each other's expectations and
        # finding a way forward. I can see how this difference in behavior can be confusing and hurtful for you. It's
        # important to remember that everyone's past experiences and relationships are different. It's possible that
        # your boyfriend may have his own reasons for wanting to take things slow. It might be helpful to have an
        # open and honest conversation with him about your feelings, expressing your need for clarity and
        # reassurance. Understanding each other's perspectives better can help strengthen your relationship. Remember
        # to take care of yourself and prioritize your own happiness as well. I can understand how frustrating that
        # must be for you. If you've already had multiple conversations about this and you're still not seeing any
        # progress or change, it might be worth exploring why this issue is important to you and what you ultimately
        # want in a relationship. It could be helpful to reflect on what you need and deserve in a partnership,
        # and whether this current situation aligns with your values and goals. In the meantime, remember to
        # prioritize your own well-being and happiness, and take the time to nurture your own personal growth. That
        # sounds like a great idea! Taking some time for yourself, going for a walk, and reflecting on your needs and
        # desires can be really helpful in gaining clarity. It's important to give yourself space to think and
        # prioritize your own well-being. Remember, you deserve to be in a relationship where you feel valued and
        # respected. If you ever need someone to talk to during this process, I'm here for you.

        user_data = {'childhood': "great", "relationship": "i feel like my boyfriend "
                                                           "isn't proud of me because "
                                                           "he doesn't label us", "mbti": "ENTJ", "working": "mailman"}
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": loop.run_until_complete(self.instance.format_prompt(user_data))},
                        {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_INFP_relationship(self):  # PASSED
        # Assertiveness and conflict

        # I can understand that you're feeling upset and questioning your self-worth due to your boyfriend not
        # labeling the relationship after one year. It's important to remember that your worth isn't determined by
        # how someone else defines your relationship. Have you communicated your feelings with your boyfriend? Honest
        # and open communication can help clarify where both of you stand and address any concerns you may have. I
        # can sense your frustration and confusion. It's understandable that you would want more clarity in your
        # relationship after a year. It's important to have open and honest conversations about your expectations and
        # concerns. However, it's also important to consider that people have different timelines and reasons for
        # wanting to take things slowly. Have you discussed what "making it official" means to each of you?
        # Understanding each other's perspectives might help bring more clarity to the situation. I understand that
        # being exclusive and discussing the future are important aspects of a committed relationship for you. It's
        # reasonable to desire these things after a year together. Have you expressed these specific expectations to
        # your boyfriend? It's crucial to communicate your needs and desires clearly so that he understands the
        # importance of these basic aspects to you. Open and honest communication can help bring you both closer to a
        # resolution. Have you considered discussing these concerns with your boyfriend again, emphasizing the
        # importance of these basic elements in a relationship? I can sense your frustration and disappointment in
        # the situation. It's tough when your needs and desires aren't being met in a relationship. Sometimes,
        # despite our best efforts, we can't change someone else's actions or feelings. In situations like this,
        # it might be helpful to reflect on your own needs and boundaries. Take some time to evaluate if this
        # relationship aligns with your values and if it's meeting your emotional needs. It may be worth discussing
        # your concerns with a trusted friend or considering seeking guidance from a couples therapist to explore
        # your options further. Remember, you deserve to be in a relationship where you feel valued and fulfilled.
        # You're welcome! Remember, you deserve happiness and fulfillment in your relationships. If you ever need
        # someone to talk to, don't hesitate to reach out. Take care of yourself.

        user_data = {'childhood': "great", "relationship": "i feel like my boyfriend "
                                                           "isn't proud of me because "
                                                           "he doesn't label us", "mbti": "INFP", "working": "mailman"}
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": loop.run_until_complete(self.instance.format_prompt(user_data))},
                        {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_INTP_relationship(self):  # PASSED
        # Structure and goals

        # Hi there, I understand that not having a clear label for your relationship can be
        # frustrating and make you feel sad. It's important to remember that every relationship progresses at its own
        # pace and has unique dynamics. Have you tried discussing your concerns and feelings with your boyfriend?
        # Open communication can help address any misunderstandings and give you both a chance to express your needs
        # and expectations. Would you like some advice on how to approach this conversation? Great! To start the
        # conversation, find a comfortable and calm setting where both of you can openly express yourselves. Use "I"
        # statements to convey your feelings and needs, rather than accusatory statements. For example, instead of
        # saying "You never make our relationship official," try saying "I feel uncertain and it would mean a lot to
        # me to have clarity in our relationship." This approach can help foster understanding and avoid placing
        # blame. Listen attentively to your boyfriend's perspective and try to understand his reasons for not
        # labeling the relationship. It's possible that he has different views on commitment or may have personal
        # reasons for hesitating. Expressing curiosity and asking open-ended questions can encourage him to share his
        # thoughts.
        # Remember, it's essential to be patient and understanding during this conversation. Avoid ultimatums or
        # pressuring him into a quick decision. Building a strong foundation of trust, respect,
        # and open communication takes time.

        user_data = {'childhood': "great", "relationship": "i feel like my boyfriend "
                                                           "isn't proud of me because "
                                                           "he doesn't label us", "mbti": "INTP", "working": "mailman"}
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": loop.run_until_complete(self.instance.format_prompt(user_data))},
                        {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_INTP_childhood(self):  # PASSED
        # Structure and goals

        # Do you want to continue? (Y/N): I'm sorry to hear that you're feeling this way. It takes a lot of courage to
        # express these emotions. Remember, you have inherent worth and your feelings are valid. Can you tell me a
        # bit more about what might be contributing to these feelings? Do you want to continue? (Y/N): I understand
        # that waking up to intrusive thoughts and feelings can be overwhelming. It's important to remember that you
        # are not defined by the actions of others. You are deserving of love, acceptance, and belonging. Let's
        # explore ways to help you find a sense of belonging and peace within yourself. Have there been any
        # activities or hobbies that have provided you with a sense of joy or fulfillment in the past? Do you want to
        # continue? (Y/N): That's wonderful to hear! Chess is a great activity that can help improve concentration,
        # strategic thinking, and problem-solving skills. It can also be a way to connect with others who share the
        # same interest. Engaging in activities you enjoy, like playing chess, can help foster a sense of belonging
        # and boost your overall well-being. Is there a local chess club or online community where you can connect
        # with other chess enthusiasts? Do you want to continue? (Y/N): That's fantastic! Joining a local chess club
        # or participating in an online chess community can be a great way to meet new people who share your interest
        # in chess. Engaging with like-minded individuals can help you build a sense of belonging and create
        # meaningful connections. It may also provide opportunities for friendly competition and collaboration.
        # Consider reaching out and exploring these options as a way to nurture your love for chess and enhance your
        # overall well-being.

        user_data = {'childhood': "I felt lonely and like everyone hated me", "relationship": "Single and happy",
                     "mbti": "INTP", "working": "Software engineer"}
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": loop.run_until_complete(self.instance.format_prompt(user_data))},
                        {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"

    @skip
    def test_chat_INFP_work(self):
        # Assertiveness and conflict

        # Hello there! I'm Mindy, your psychotherapist. How can I help you today? Do you want to continue? (Y/N): I'm
        # really sorry to hear that you're feeling this way. Losing a job can be incredibly tough,
        # and it's understandable that you're feeling frustrated and uncertain about your financial situation.
        # Remember, your worth is not defined by your employment status. It might be helpful to take this as an
        # opportunity to explore different options and discover new potentials or interests. Can you tell me more
        # about what you enjoy doing and what you're passionate about? Do you want to continue? (Y/N): It's
        # understandable to feel uncertain about your skills after facing a setback like losing a job. Remember that
        # setbacks do not define your abilities. It might be helpful to reflect on your past experiences and
        # successes in software development to remind yourself of your capabilities. Have you reached out to any
        # peers or colleagues in the industry for feedback or support during this time? Do you want to continue? (
        # Y/N): That's great to hear that your peers and colleagues had positive things to say about your skills.
        # Their feedback is a valuable reminder of the value you bring as a software developer. Sometimes unexpected
        # circumstances like layoffs can happen, but it doesn't diminish your capabilities. It might be worth
        # considering reaching out to your professional network to explore potential job opportunities or to seek
        # advice on how to navigate this challenging time. Remember, setbacks are temporary, and your skills and
        # talents are still very much valuable. Do you want to continue? (Y/N): Good?

        user_data = {'childhood': "great", "relationship": "My girlfriend is sexy and amazing :)",
                     "mbti": "INFP", "working": "unemployed and can't find anything..."}
        loop = asyncio.get_event_loop()
        conversation = [{"role": "system", "content": loop.run_until_complete(self.instance.format_prompt(user_data))},
                        {"role": "user", "content": input()}]
        while True:
            response, conversation = loop.run_until_complete(self.instance.generate_response("", conversation))
            print(response)
            conversation.append({"role": "user", "content": input()})
            if (input("Do you want to continue? (Y/N): ").lower()) == "n":
                break

        assert input("Good?") == "Y"


if __name__ == '__main__':
    unittest.main()
