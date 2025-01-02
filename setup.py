from setuptools import setup, find_packages

setup(
    name="discordnotify-klubbezgusci",
    version="1.0.0",
    description="A library for managing Discord notifications with a custom bot, utilizing Supabase for data storage.",
    author="Tomasz Respondek",
    author_email="your_email@example.com",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "requests",
        "pytz",
        "supabase-py",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)