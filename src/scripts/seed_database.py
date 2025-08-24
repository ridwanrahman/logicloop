"""
Database seeding script for logic_loop question bank application.
Run this script to populate the database with realistic mock data.

Usage:
    python manage.py shell < scripts/seed_database.py
    OR
    python manage.py runscript seed_database  $ if using django-extensions
"""
import os
import sys
import random
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from faker import Faker
from pathlib import Path

# Import your models here
from users.models import UserProfile
from categories.models import Category, Tag
from submissions.models import Submission, SubmissionResult
from users.models import User
from questions.models import Difficulty, Question, TestCase, QuestionExample
from progress.models import UserProgress, Achievement, UserAchievement
from discussion.models import Discussion, DiscussionReply, Vote

fake = Faker()
# User = get_user_model()
# # Sample data constants
PROGRAMMING_LANGUAGES = [
    'python', 'java', 'cpp', 'c', 'javascript', 'go', 'rust'
]

SKILL_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert']
SAMPLE_CODE_SOLUTIONS = {
    'python': '''def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []''',
    'java': '''public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[] { map.get(complement), i };
        }
        map.put(nums[i], i);
    }
    return new int[0];
}''',

    'cpp': '''vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> map;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (map.find(complement) != map.end()) {
            return {map[complement], i};
        }
        map[nums[i]] = i;
    }
    return {};
}'''
}
SUBMISSION_STATUSES = [
    'accepted', 'wrong_answer', 'time_limit_exceeded',
    'memory_limit_exceeded', 'runtime_error', 'compilation_error'
]

CATEGORIES_DATA = [
    {
        'name': 'Arrays & Strings',
        'description': 'Problems involving array manipulation and string processing',
        'icon': 'list',
        'color': '#007bff'
    },
    {
        'name': 'Linked Lists',
        'description': 'Single, double, and circular linked list problems',
        'icon': 'link',
        'color': '#28a745'
    },
    {
        'name': 'Trees & Graphs',
        'description': 'Binary trees, BSTs, graphs, and tree traversal problems',
        'icon': 'tree',
        'color': '#17a2b8'
    },
    {
        'name': 'Dynamic Programming',
        'description': 'Optimization problems using dynamic programming techniques',
        'icon': 'layers',
        'color': '#ffc107'
    },
    {
        'name': 'Sorting & Searching',
        'description': 'Various sorting algorithms and search techniques',
        'icon': 'search',
        'color': '#6f42c1'
    },
    {
        'name': 'Hash Tables',
        'description': 'Problems involving hash maps and hash sets',
        'icon': 'grid',
        'color': '#fd7e14'
    },
    {
        'name': 'Recursion & Backtracking',
        'description': 'Recursive solutions and backtracking algorithms',
        'icon': 'repeat',
        'color': '#e83e8c'
    },
    {
        'name': 'Math & Logic',
        'description': 'Mathematical problems and logical reasoning',
        'icon': 'calculator',
        'color': '#20c997'
    }
]

TAGS_DATA = [
    'array', 'string', 'hash-table', 'dynamic-programming', 'math', 'two-pointers',
    'binary-search', 'sorting', 'greedy', 'depth-first-search', 'breadth-first-search',
    'tree', 'stack', 'heap', 'graph', 'backtracking', 'bit-manipulation', 'recursion',
    'sliding-window', 'divide-and-conquer', 'linked-list', 'binary-tree', 'trie',
    'union-find', 'monotonic-stack', 'prefix-sum', 'simulation', 'game-theory'
]
QUESTIONS_DATA = [
    {
        'title': 'Two Sum',
        'category': 'Arrays & Strings',
        'difficulty': 'Easy',
        'tags': ['array', 'hash-table'],
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
        'problem_statement': '''You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.''',
        'input_format': 'nums = [2,7,11,15], target = 9',
        'output_format': '[0,1]',
        'constraints': '2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9',
        'hints': ['Try using a hash table to store the complement of each number', 'For each number, check if target - number exists in the hash table'],
        'examples': [
            {
                'input': 'nums = [2,7,11,15], target = 9',
                'output': '[0,1]',
                'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].'
            }
        ],
        'test_cases': [
            {'input': '[2,7,11,15]\n9', 'output': '[0,1]', 'is_sample': True},
            {'input': '[3,2,4]\n6', 'output': '[1,2]', 'is_sample': False},
            {'input': '[3,3]\n6', 'output': '[0,1]', 'is_sample': False}
        ]
    },
    {
        'title': 'Reverse Linked List',
        'category': 'Linked Lists',
        'difficulty': 'Easy',
        'tags': ['linked-list', 'recursion'],
        'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
        'problem_statement': 'Reverse a singly linked list iteratively or recursively.',
        'input_format': 'head = [1,2,3,4,5]',
        'output_format': '[5,4,3,2,1]',
        'constraints': 'The number of nodes in the list is the range [0, 5000].\n-5000 <= Node.val <= 5000',
        'hints': ['Use three pointers: prev, current, and next', 'Or solve it recursively'],
        'examples': [
            {
                'input': 'head = [1,2,3,4,5]',
                'output': '[5,4,3,2,1]',
                'explanation': 'Reverse the linked list from 1->2->3->4->5 to 5->4->3->2->1'
            }
        ],
        'test_cases': [
            {'input': '[1,2,3,4,5]', 'output': '[5,4,3,2,1]', 'is_sample': True},
            {'input': '[1,2]', 'output': '[2,1]', 'is_sample': False},
            {'input': '[]', 'output': '[]', 'is_sample': False}
        ]
    },
    {
        'title': 'Maximum Subarray',
        'category': 'Dynamic Programming',
        'difficulty': 'Medium',
        'tags': ['array', 'dynamic-programming', 'divide-and-conquer'],
        'description': 'Given an integer array nums, find the contiguous subarray which has the largest sum and return its sum.',
        'problem_statement': 'Find the contiguous subarray within a one-dimensional array of numbers that has the largest sum.',
        'input_format': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
        'output_format': '6',
        'constraints': '1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4',
        'hints': ['Use Kadane\'s algorithm', 'Keep track of current sum and maximum sum'],
        'examples': [
            {
                'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
                'output': '6',
                'explanation': '[4,-1,2,1] has the largest sum = 6.'
            }
        ],
        'test_cases': [
            {'input': '[-2,1,-3,4,-1,2,1,-5,4]', 'output': '6', 'is_sample': True},
            {'input': '[1]', 'output': '1', 'is_sample': False},
            {'input': '[5,4,-1,7,8]', 'output': '23', 'is_sample': False}
        ]
    },
    {
        'title': 'Binary Tree Inorder Traversal',
        'category': 'Trees & Graphs',
        'difficulty': 'Easy',
        'tags': ['tree', 'depth-first-search', 'binary-tree', 'stack'],
        'description': 'Given the root of a binary tree, return the inorder traversal of its nodes values.',
        'problem_statement': 'Traverse the binary tree in inorder fashion: left, root, right.',
        'input_format': 'root = [1,null,2,3]',
        'output_format': '[1,3,2]',
        'constraints': 'The number of nodes in the tree is in the range [0, 100].\n-100 <= Node.val <= 100',
        'hints': ['Use recursion or stack-based iterative approach', 'Inorder: left -> root -> right'],
        'examples': [
            {
                'input': 'root = [1,null,2,3]',
                'output': '[1,3,2]',
                'explanation': 'Inorder traversal: left subtree, root, right subtree'
            }
        ],
        'test_cases': [
            {'input': '[1,null,2,3]', 'output': '[1,3,2]', 'is_sample': True},
            {'input': '[]', 'output': '[]', 'is_sample': False},
            {'input': '[1]', 'output': '[1]', 'is_sample': False}
        ]
    },
    {
        'title': 'Valid Parentheses',
        'category': 'Arrays & Strings',
        'difficulty': 'Easy',
        'tags': ['string', 'stack'],
        'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.',
        'problem_statement': 'An input string is valid if: Open brackets must be closed by the same type of brackets and in the correct order.',
        'input_format': 's = "()[]{}"',
        'output_format': 'true',
        'constraints': '1 <= s.length <= 10^4\ns consists of parentheses only \'()[]{}\'.',
        'hints': ['Use a stack to keep track of opening brackets', 'When you see a closing bracket, check if it matches the most recent opening bracket'],
        'examples': [
            {
                'input': 's = "()[]{}"',
                'output': 'true',
                'explanation': 'All brackets are properly matched and nested.'
            }
        ],
        'test_cases': [
            {'input': '"()[]{}"', 'output': 'true', 'is_sample': True},
            {'input': '"([)]"', 'output': 'false', 'is_sample': False},
            {'input': '"{[]}"', 'output': 'true', 'is_sample': False}
        ]
    }
]


def create_users(count=50):
    print("🧹 Cleaning User table...")
    User.objects.all().delete()

    print(f"👥 Creating {count} users...")
    users = []
    # Create admin user
    admin = User.objects.create_superuser(
        username='ridwan',
        email='ridwan@test.com',
        password='ridwan',
        first_name='Admin',
        last_name='User',
        total_points=0,
        problems_solved=0
    )
    # Create admin profile
    UserProfile.objects.create(
        user=admin,
        preferred_language='python',
        skill_level='expert',
        location='San Francisco, CA',
        website='https://logic_loop.com',
        is_public=True
    )
    users.append(admin)

    # Create regular users
    for i in range(count - 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        email = fake.email()

        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            first_name=first_name,
            last_name=last_name,
            bio=fake.text(max_nb_chars=200) if random.choice([True, False]) else '',
            github_username=f"{username}" if random.choice([True, False]) else '',
            linkedin_profile=f"https://linkedin.com/in/{username}" if random.choice([True, False]) else '',
            total_points=random.randint(0, 5000),
            problems_solved=random.randint(0, 50)
        )
        users.append(user)

        # Create user profile
        UserProfile.objects.create(
            user=user,
            preferred_language=random.choice(PROGRAMMING_LANGUAGES),
            skill_level=random.choice(SKILL_LEVELS),
            location=fake.city() + ", " + fake.state_abbr(),
            website=fake.url() if random.choice([True, False]) else '',
            is_public=random.choice([True, True, True, False])  # 75% public
        )

    print(f"✅ Created {len(users)} users!")
    return users


def create_difficulties():
    """Create difficulty levels"""
    # remove from db
    print("🧹 Cleaning Difficulty table...")
    Difficulty.objects.all().delete()

    print("📊 Creating difficulty levels...")

    difficulties = [
        {'name': 'Easy', 'level': 1, 'color': '#28a745', 'points': 10},
        {'name': 'Medium', 'level': 2, 'color': '#ffc107', 'points': 25},
        {'name': 'Hard', 'level': 3, 'color': '#dc3545', 'points': 50}
    ]

    created_difficulties = []
    for diff_data in difficulties:
        difficulty = Difficulty.objects.create(**diff_data)
        created_difficulties.append(difficulty)

    print("✅ Created difficulty levels!")
    return created_difficulties


def create_categories_and_tags():
    """Create categories and tags"""
    print("🧹 Cleaning Category table...")
    Category.objects.all().delete()
    print("🧹 Cleaning Tag table...")
    Tag.objects.all().delete()

    print("🏷️  Creating categories and tags...")

    # Create categories
    categories = []
    for i, cat_data in enumerate(CATEGORIES_DATA):
        cat_data['slug'] = slugify(cat_data['name'])
        cat_data['order'] = i
        category = Category.objects.create(**cat_data)
        categories.append(category)

    # Create tags
    tags = []
    for tag_name in TAGS_DATA:
        tag = Tag.objects.create(
            name=tag_name,
            slug=slugify(tag_name),
            description=f"Problems related to {tag_name}",
            color=fake.hex_color()
        )
        tags.append(tag)

    print(f"✅ Created {len(categories)} categories and {len(tags)} tags!")
    return categories, tags


def create_questions(categories, tags, difficulties, users):
    """Create questions with examples and test cases"""
    print("🧹 Cleaning questions table...")
    Question.objects.all().delete()
    print("🧹 Cleaning test case table...")
    TestCase.objects.all().delete()


    print("❓ Creating questions...")
    questions = []
    # Create predefined questions
    for q_data in QUESTIONS_DATA:
        category = next(c for c in categories if c.name == q_data['category'])
        difficulty = next(d for d in difficulties if d.name == q_data['difficulty'])
        creator = random.choice(users[:5])  # Use first 5 users as creators

        question = Question.objects.create(
            title=q_data['title'],
            slug=slugify(q_data['title']),
            description=q_data['description'],
            problem_statement=q_data['problem_statement'],
            input_format=q_data['input_format'],
            output_format=q_data['output_format'],
            constraints=q_data['constraints'],
            category=category,
            difficulty=difficulty,
            created_by=creator,
            hints=q_data['hints'],
            time_limit=random.randint(1, 10),
            memory_limit=random.randint(128, 512),
            total_submissions=random.randint(100, 5000),
            successful_submissions=random.randint(50, 2000)
        )

        # Add tags
        question_tags = [t for t in tags if t.name in q_data['tags']]
        question.tags.set(question_tags)

        # Create examples
        for i, example in enumerate(q_data['examples']):
            QuestionExample.objects.create(
                question=question,
                input_example=example['input'],
                output_example=example['output'],
                explanation=example['explanation'],
                order=i
            )

        # Create test cases
        for i, test_case in enumerate(q_data['test_cases']):
            TestCase.objects.create(
                question=question,
                input_data=test_case['input'],
                expected_output=test_case['output'],
                is_sample=test_case['is_sample'],
                is_hidden=not test_case['is_sample'],
                points=1 if test_case['is_sample'] else random.randint(1, 5)
            )

        questions.append(question)

    # Create additional random questions
    additional_count = 25
    for i in range(additional_count):
        title = fake.sentence(nb_words=4).replace('.', '')
        question = Question.objects.create(
            title=title,
            slug=slugify(title),
            description=fake.paragraph(nb_sentences=3),
            problem_statement=fake.paragraph(nb_sentences=5),
            input_format=fake.sentence(),
            output_format=fake.sentence(),
            constraints=fake.paragraph(nb_sentences=2),
            category=random.choice(categories),
            difficulty=random.choice(difficulties),
            created_by=random.choice(users[:10]),
            hints=[fake.sentence() for _ in range(random.randint(1, 3))],
            time_limit=random.randint(1, 10),
            memory_limit=random.randint(128, 512),
            total_submissions=random.randint(10, 1000),
            successful_submissions=random.randint(5, 500)
        )

        # Add random tags
        question.tags.set(random.sample(tags, random.randint(1, 4)))

        # Create test cases
        for j in range(random.randint(3, 8)):
            TestCase.objects.create(
                question=question,
                input_data=fake.text(max_nb_chars=100),
                expected_output=fake.text(max_nb_chars=50),
                is_sample=j < 2,  # First 2 are sample
                is_hidden=j >= 2,
                points=random.randint(1, 5)
            )

        questions.append(question)

    print(f"✅ Created {len(questions)} questions!")
    return questions


def create_submissions(users, questions):
    """Create submissions and results"""
    print("🧹 Cleaning submissions table...")
    Submission.objects.all().delete()

    print("📝 Creating submissions...")
    submissions = []
    for user in random.sample(users, min(30, len(users))):  # 30 random users
        user_questions = random.sample(questions, random.randint(1, 15))

        for question in user_questions:
            # Create 1-5 submissions per user per question
            num_submissions = random.randint(1, 5)

            for attempt in range(num_submissions):
                language = random.choice(PROGRAMMING_LANGUAGES)
                status = random.choice(SUBMISSION_STATUSES)

                # Better success rate for later attempts
                if attempt > 0 and random.random() < 0.6:
                    status = 'accepted'

                submission = Submission.objects.create(
                    user=user,
                    question=question,
                    code=SAMPLE_CODE_SOLUTIONS.get(language, fake.text(max_nb_chars=500)),
                    language=language,
                    status=status,
                    execution_time=random.uniform(0.1, 2.0) if status == 'accepted' else None,
                    memory_used=random.randint(10, 100) if status == 'accepted' else None,
                    points_earned=question.difficulty.points if status == 'accepted' else 0,
                    passed_test_cases=random.randint(0,
                                                     question.test_cases.count()) if status != 'accepted' else question.test_cases.count(),
                    total_test_cases=question.test_cases.count(),
                    error_message=fake.sentence() if status != 'accepted' else '',
                    created_at=timezone.make_aware(fake.date_time_between(start_date='-30d', end_date='now'))
                )

                # Create submission results for each test case
                for test_case in question.test_cases.all():
                    result_status = status
                    if status == 'accepted':
                        result_status = 'accepted'
                    elif status == 'wrong_answer':
                        result_status = random.choice(['accepted', 'wrong_answer'])

                    SubmissionResult.objects.create(
                        submission=submission,
                        test_case=test_case,
                        status=result_status,
                        execution_time=random.uniform(0.05, 0.5) if result_status == 'accepted' else None,
                        memory_used=random.randint(5, 50) if result_status == 'accepted' else None,
                        output=test_case.expected_output if result_status == 'accepted' else fake.text(max_nb_chars=50),
                        error_message='' if result_status == 'accepted' else fake.sentence()
                    )

                submissions.append(submission)

    print(f"✅ Created {len(submissions)} submissions!")
    return submissions


def create_user_progress(users, questions, submissions):
    """Create user progress tracking"""
    print("🧹 Cleaning userprogress table...")
    UserProgress.objects.all().delete()

    print("📈 Creating user progress...")
    progress_records = []
    for user in users:
        user_submissions = [s for s in submissions if s.user == user]
        attempted_questions = list(set([s.question for s in user_submissions]))

        for question in attempted_questions:
            question_submissions = [s for s in user_submissions if s.question == question]
            best_submission = max(question_submissions, key=lambda s: s.points_earned, default=None)

            status = 'not_started'
            if question_submissions:
                if any(s.status == 'accepted' for s in question_submissions):
                    status = 'solved'
                elif any(s.points_earned > 0 for s in question_submissions):
                    status = 'partially_solved'
                else:
                    status = 'in_progress'

            first_solved = None
            if status == 'solved':
                accepted_submissions = [s for s in question_submissions if s.status == 'accepted']
                if accepted_submissions:
                    first_solved = min(accepted_submissions, key=lambda s: s.created_at).created_at

            progress = UserProgress.objects.create(
                user=user,
                question=question,
                status=status,
                attempts=len(question_submissions),
                best_submission=best_submission,
                points_earned=best_submission.points_earned if best_submission else 0,
                first_solved_at=first_solved
            )
            progress_records.append(progress)

    print(f"✅ Created {len(progress_records)} progress records!")
    return progress_records


def create_achievements(users):
    """Create achievements and user achievements"""
    print("🧹 Cleaning achievements table...")
    Achievement.objects.all().delete()
    print("🧹 Cleaning Userachievements table...")
    UserAchievement.objects.all().delete()

    print("🏆 Creating achievements...")
    achievements = [
        {
            'name': 'First Steps',
            'description': 'Solve your first problem',
            'icon': 'star',
            'color': '#ffd700',
            'required_problems_solved': 1
        },
        {
            'name': 'Getting Started',
            'description': 'Solve 5 problems',
            'icon': 'trophy',
            'color': '#ffd700',
            'required_problems_solved': 5
        },
        {
            'name': 'Problem Solver',
            'description': 'Solve 25 problems',
            'icon': 'award',
            'color': '#ffd700',
            'required_problems_solved': 25
        },
        {
            'name': 'Point Hunter',
            'description': 'Earn 500 points',
            'icon': 'target',
            'color': '#28a745',
            'required_points': 500
        },
        {
            'name': 'Array Master',
            'description': 'Solve 10 array problems',
            'icon': 'grid',
            'color': '#007bff'
        }
    ]

    created_achievements = []
    for ach_data in achievements:
        achievement = Achievement.objects.create(**ach_data)
        created_achievements.append(achievement)

    # Award achievements to users
    user_achievements = []
    for user in users:
        for achievement in created_achievements:
            should_award = False

            if achievement.required_problems_solved:
                should_award = user.problems_solved >= achievement.required_problems_solved
            elif achievement.required_points:
                should_award = user.total_points >= achievement.required_points
            else:
                should_award = random.choice([True, False])  # Random for category-specific

            if should_award:
                user_ach = UserAchievement.objects.create(
                    user=user,
                    achievement=achievement,
                    earned_at=fake.date_time_between(start_date='-30d', end_date='now')
                )
                user_achievements.append(user_ach)

    print(f"✅ Created {len(created_achievements)} achievements and awarded {len(user_achievements)} to users!")
    return created_achievements, user_achievements


def create_discussions(users, questions):
    """Create discussions and replies"""
    print("🧹 Cleaning discussions table...")
    Discussion.objects.all().delete()
    print("🧹 Cleaning DiscussionReply table...")
    DiscussionReply.objects.all().delete()
    print("🧹 Cleaning Vote table...")
    Vote.objects.all().delete()

    print("💬 Creating discussions...")
    discussions = []
    replies = []
    # Create discussions for random questions
    sample_questions = random.sample(questions, min(15, len(questions)))

    for question in sample_questions:
        num_discussions = random.randint(1, 4)

        for i in range(num_discussions):
            discussion = Discussion.objects.create(
                question=question,
                author=random.choice(users),
                title=fake.sentence(nb_words=6).replace('.', '?'),
                content=fake.paragraph(nb_sentences=random.randint(2, 5)),
                is_pinned=i == 0 and random.choice([True, False]),  # Sometimes pin first discussion
                views=random.randint(10, 500),
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            )
            discussions.append(discussion)

            # Create replies
            num_replies = random.randint(0, 8)
            for j in range(num_replies):
                reply = DiscussionReply.objects.create(
                    discussion=discussion,
                    author=random.choice(users),
                    content=fake.paragraph(nb_sentences=random.randint(1, 3)),
                    upvotes=random.randint(0, 20),
                    downvotes=random.randint(0, 5),
                    created_at=fake.date_time_between(start_date=discussion.created_at, end_date='now')
                )
                replies.append(reply)

                # Create some votes
                voters = random.sample(users, min(random.randint(0, 10), len(users)))
                for voter in voters:
                    if voter != reply.author:  # Can't vote on own reply
                        Vote.objects.create(
                            user=voter,
                            reply=reply,
                            vote_type=random.choice(['upvote', 'downvote'])
                        )

    print(f"✅ Created {len(discussions)} discussions and {len(replies)} replies!")
    return discussions, replies


users = create_users()
difficulties = create_difficulties()
categories, tags = create_categories_and_tags()
questions = create_questions(categories, tags, difficulties, users)
submissions = create_submissions(users, questions)
user_progress = create_user_progress(users, questions, submissions)
created_achievements, user_achievements = create_achievements(users)
discussions, replies = create_discussions(users, questions)

# if __name__ == "__main__":
#     print("inside main")
#     import os
#     import sys
#     import django
#     from pathlib import Path
#
#     # Add the src directory to Python path
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     sys.path.append(str(BASE_DIR))
#
#     # Set up Django environment
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logic_loop.settings')
#     django.setup()
#
#     # Now you can import your Django models
#     from users.models import User
#     from questions.models import Difficulty
#     users = create_users()
#
#     difficulties = create_difficulties()


    