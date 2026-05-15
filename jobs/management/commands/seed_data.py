"""
Management command to wipe existing data and seed realistic fake data.

Usage:
    python manage.py seed_data

Place this file at:
    jobs/management/commands/seed_data.py

Also create these empty files if they don't exist:
    jobs/management/__init__.py
    jobs/management/commands/__init__.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import Job, Application
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Wipe all data and seed realistic fake job portal data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🗑️  Deleting existing data...')
        Application.objects.all().delete()
        Job.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('✅ Existing data cleared'))

        # -----------------------------------------------
        # EMPLOYERS
        # -----------------------------------------------
        employers_data = [
            {
                'email': 'hr@careerstackmailinfosys.com',
                'username': 'infosys_hr',
                'password': 'Test@1234',
                'company_name': 'Infosys',
                'company_website': 'https://www.infosys.com',
                'company_description': 'Infosys is a global leader in next-generation digital services and consulting. We help clients in more than 50 countries navigate their digital transformation.',
                'phone': '9876543210',
            },
            {
                'email': 'careers@careerstacktcs.com',
                'username': 'tcs_careers',
                'password': 'Test@1234',
                'company_name': 'Tata Consultancy Services',
                'company_website': 'https://www.tcs.com',
                'company_description': 'TCS is an IT services, consulting and business solutions organization that has been partnering with many of the world\'s largest businesses for over 55 years.',
                'phone': '9123456780',
            },
            {
                'email': 'jobs@careerstackflipkart.com',
                'username': 'flipkart_jobs',
                'password': 'Test@1234',
                'company_name': 'Flipkart',
                'company_website': 'https://www.flipkart.com',
                'company_description': 'Flipkart is India\'s leading e-commerce marketplace, offering over 150 million products across 80+ categories to 400 million+ registered customers.',
                'phone': '9988776655',
            },
            {
                'email': 'talent@careerstackrazorpay.com',
                'username': 'razorpay_talent',
                'password': 'Test@1234',
                'company_name': 'Razorpay',
                'company_website': 'https://razorpay.com',
                'company_description': 'Razorpay is India\'s leading full-stack financial solutions company, enabling businesses to accept, process and disburse payments with its product suite.',
                'phone': '9001122334',
            },
            {
                'email': 'hr@careerstackzomato.com',
                'username': 'zomato_hr',
                'password': 'Test@1234',
                'company_name': 'Zomato',
                'company_website': 'https://www.zomato.com',
                'company_description': 'Zomato is an Indian multinational restaurant aggregator and food delivery company, operating in 1000+ cities across India and internationally.',
                'phone': '9871234560',
            },
        ]

        employers = []
        for data in employers_data:
            user = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password=data['password'],
                role='employer',
                company_name=data['company_name'],
                company_website=data['company_website'],
                company_description=data['company_description'],
                phone=data['phone'],
            )
            employers.append(user)
            self.stdout.write(f'  👔 Employer: {data["company_name"]}')

        # -----------------------------------------------
        # JOB SEEKERS
        # -----------------------------------------------
        seekers_data = [
            {
                'email': 'arjun.sharma@careerstackmail.com',
                'username': 'arjun_sharma',
                'password': 'Test@1234',
                'phone': '9812345678',
                'skills': 'Python, Django, REST API, PostgreSQL, Docker',
            },
            {
                'email': 'priya.mehta@careerstackmail.com',
                'username': 'priya_mehta',
                'password': 'Test@1234',
                'phone': '9923456781',
                'skills': 'React, JavaScript, TypeScript, Tailwind CSS, Node.js',
            },
            {
                'email': 'rahul.verma@careerstackmail.com',
                'username': 'rahul_verma',
                'password': 'Test@1234',
                'phone': '9734561290',
                'skills': 'Java, Spring Boot, Microservices, Kafka, AWS',
            },
            {
                'email': 'neha.joshi@careerstackmail.com',
                'username': 'neha_joshi',
                'password': 'Test@1234',
                'phone': '9845672310',
                'skills': 'Data Science, Python, Machine Learning, Pandas, TensorFlow',
            },
            {
                'email': 'karan.patel@careerstackmail.com',
                'username': 'karan_patel',
                'password': 'Test@1234',
                'phone': '9900112233',
                'skills': 'DevOps, Kubernetes, CI/CD, Terraform, Linux',
            },
            {
                'email': 'sneha.rao@careerstackmail.com',
                'username': 'sneha_rao',
                'password': 'Test@1234',
                'phone': '9765432109',
                'skills': 'Flutter, Dart, Android, iOS, Firebase',
            },
            {
                'email': 'amit.singh@careerstackmail.com',
                'username': 'amit_singh',
                'password': 'Test@1234',
                'phone': '9654321098',
                'skills': 'Node.js, Express, MongoDB, GraphQL, Redis',
            },
            {
                'email': 'divya.kumar@careerstackmail.com',
                'username': 'divya_kumar',
                'password': 'Test@1234',
                'phone': '9543210987',
                'skills': 'UI/UX Design, Figma, Adobe XD, Prototyping, User Research',
            },
        ]

        seekers = []
        for data in seekers_data:
            user = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password=data['password'],
                role='job_seeker',
                phone=data['phone'],
                skills=data['skills'],
            )
            seekers.append(user)
            self.stdout.write(f'  👤 Job Seeker: {data["username"]}')

        # -----------------------------------------------
        # JOBS
        # -----------------------------------------------
        jobs_data = [
            # Infosys jobs
            {
                'employer': employers[0],
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to join our backend engineering team. You will be responsible for building scalable APIs, optimizing database performance, and mentoring junior developers.',
                'requirements': '4+ years of Python experience. Strong knowledge of Django or FastAPI. Experience with PostgreSQL and Redis. Familiarity with Docker and microservices architecture.',
                'location': 'Bangalore',
                'salary_min': 1200000,
                'salary_max': 1800000,
                'job_type': 'full_time',
                'experience_level': 'senior',
                'skills_required': 'Python, Django, PostgreSQL, Docker, Redis',
                'deadline': date.today() + timedelta(days=30),
            },
            {
                'employer': employers[0],
                'title': 'DevOps Engineer',
                'description': 'Join our infrastructure team to build and maintain CI/CD pipelines, manage cloud deployments on AWS, and ensure high availability of our production systems.',
                'requirements': '3+ years in DevOps. Hands-on experience with Kubernetes and Terraform. Strong Linux skills. AWS certifications preferred.',
                'location': 'Hyderabad',
                'salary_min': 1000000,
                'salary_max': 1600000,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'skills_required': 'Kubernetes, Terraform, AWS, CI/CD, Linux, Docker',
                'deadline': date.today() + timedelta(days=25),
            },
            # TCS jobs
            {
                'employer': employers[1],
                'title': 'Java Backend Developer',
                'description': 'We need a skilled Java developer to work on enterprise-grade applications for our banking clients. You will design and implement microservices using Spring Boot.',
                'requirements': '3-6 years of Java development experience. Proficiency in Spring Boot and Hibernate. Experience with Kafka and REST APIs. Good communication skills.',
                'location': 'Mumbai',
                'salary_min': 900000,
                'salary_max': 1400000,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'skills_required': 'Java, Spring Boot, Kafka, Microservices, REST API',
                'deadline': date.today() + timedelta(days=20),
            },
            {
                'employer': employers[1],
                'title': 'Data Analyst Intern',
                'description': 'Exciting internship opportunity for final year students or fresh graduates to work with our data analytics team. You will analyze large datasets and create dashboards for business insights.',
                'requirements': 'Pursuing or completed B.Tech/MCA. Knowledge of Python and SQL. Familiarity with Power BI or Tableau is a plus.',
                'location': 'Pune',
                'salary_min': 25000,
                'salary_max': 40000,
                'job_type': 'internship',
                'experience_level': 'entry',
                'skills_required': 'Python, SQL, Power BI, Excel, Data Analysis',
                'deadline': date.today() + timedelta(days=15),
            },
            # Flipkart jobs
            {
                'employer': employers[2],
                'title': 'React Frontend Engineer',
                'description': 'Build the next generation of shopping experiences for millions of Indians. You will work on Flipkart\'s web platform, implementing new features and optimizing performance.',
                'requirements': '2+ years of React experience. Strong JavaScript and TypeScript skills. Experience with Redux and REST APIs. Eye for UI/UX detail.',
                'location': 'Bangalore',
                'salary_min': 1500000,
                'salary_max': 2500000,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'skills_required': 'React, TypeScript, Redux, JavaScript, REST API',
                'deadline': date.today() + timedelta(days=35),
            },
            {
                'employer': employers[2],
                'title': 'Mobile Developer (Flutter)',
                'description': 'Join Flipkart\'s mobile team to build cross-platform shopping apps used by 400M+ users. You will own features end-to-end from design to production.',
                'requirements': '2+ years Flutter development. Strong Dart skills. Experience with Firebase and REST APIs. Published apps on Play Store or App Store preferred.',
                'location': 'Remote',
                'salary_min': 1200000,
                'salary_max': 2000000,
                'job_type': 'remote',
                'experience_level': 'mid',
                'skills_required': 'Flutter, Dart, Firebase, Android, iOS',
                'deadline': date.today() + timedelta(days=28),
            },
            # Razorpay jobs
            {
                'employer': employers[3],
                'title': 'Backend Engineer - Payments',
                'description': 'Work on the core payments infrastructure processing millions of transactions daily. You will design fault-tolerant systems, optimize latency, and build new payment integrations.',
                'requirements': '3+ years backend experience. Strong knowledge of distributed systems. Proficiency in Node.js or Go. Experience with high-throughput systems is a must.',
                'location': 'Bangalore',
                'salary_min': 2000000,
                'salary_max': 3500000,
                'job_type': 'full_time',
                'experience_level': 'senior',
                'skills_required': 'Node.js, Distributed Systems, PostgreSQL, Redis, AWS',
                'deadline': date.today() + timedelta(days=22),
            },
            {
                'employer': employers[3],
                'title': 'Machine Learning Engineer',
                'description': 'Build ML models for fraud detection, credit scoring, and personalization at Razorpay. You will work closely with data engineers and product teams.',
                'requirements': 'Strong foundation in ML and statistics. Experience with Python and TensorFlow or PyTorch. Familiarity with MLOps and model deployment.',
                'location': 'Bangalore',
                'salary_min': 1800000,
                'salary_max': 3000000,
                'job_type': 'full_time',
                'experience_level': 'senior',
                'skills_required': 'Python, Machine Learning, TensorFlow, MLOps, SQL',
                'deadline': date.today() + timedelta(days=18),
            },
            # Zomato jobs
            {
                'employer': employers[4],
                'title': 'UI/UX Designer',
                'description': 'Design delightful experiences for Zomato\'s food ordering platform. You will conduct user research, create wireframes and prototypes, and collaborate with developers to ship pixel-perfect designs.',
                'requirements': '2+ years UX design experience. Expert in Figma. Strong portfolio showing end-to-end design work. Understanding of mobile-first design principles.',
                'location': 'Gurgaon',
                'salary_min': 800000,
                'salary_max': 1400000,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'skills_required': 'Figma, UI/UX Design, Prototyping, User Research, Adobe XD',
                'deadline': date.today() + timedelta(days=40),
            },
            {
                'employer': employers[4],
                'title': 'Full Stack Developer (Contract)',
                'description': 'We need a contractor to help build internal tools for our logistics and delivery operations team. The role is for 6 months with possibility of extension.',
                'requirements': '3+ years full stack experience. Comfortable with React and Node.js. Experience with MongoDB. Ability to work independently.',
                'location': 'Remote',
                'salary_min': 80000,
                'salary_max': 120000,
                'job_type': 'contract',
                'experience_level': 'mid',
                'skills_required': 'React, Node.js, MongoDB, Express, REST API',
                'deadline': date.today() + timedelta(days=12),
            },
        ]

        jobs = []
        for data in jobs_data:
            job = Job.objects.create(**data)
            jobs.append(job)
            self.stdout.write(f'  💼 Job: {data["title"]} @ {data["employer"].company_name}')

        # -----------------------------------------------
        # APPLICATIONS
        # -----------------------------------------------
        applications_data = [
            # Arjun applies to Python and DevOps jobs
            {'applicant': seekers[0], 'job': jobs[0], 'status': 'shortlisted',
             'cover_letter': 'I have 5 years of Python and Django experience and have built REST APIs serving 1M+ requests/day. Excited to bring this to Infosys.',
             'employer_note': 'Strong profile, schedule technical round.'},
            {'applicant': seekers[0], 'job': jobs[1], 'status': 'reviewed',
             'cover_letter': 'I have hands-on experience with Kubernetes and AWS, managing production clusters for 3 years.',
             'employer_note': ''},

            # Priya applies to React and Full Stack jobs
            {'applicant': seekers[1], 'job': jobs[4], 'status': 'pending',
             'cover_letter': 'React is my core strength. I have built e-commerce UIs with 100K+ daily users and love optimizing web performance.',
             'employer_note': ''},
            {'applicant': seekers[1], 'job': jobs[9], 'status': 'accepted',
             'cover_letter': 'Full stack is my comfort zone. I can start immediately and work independently on the logistics tool.',
             'employer_note': 'Perfect fit for the contract role. Offer sent.'},

            # Rahul applies to Java and Backend jobs
            {'applicant': seekers[2], 'job': jobs[2], 'status': 'reviewed',
             'cover_letter': 'I have 4 years of Java and Spring Boot experience in the banking domain. Familiar with Kafka-based event-driven systems.',
             'employer_note': 'Good domain experience.'},
            {'applicant': seekers[2], 'job': jobs[6], 'status': 'rejected',
             'cover_letter': 'I want to transition into payments infrastructure and have strong distributed systems knowledge.',
             'employer_note': 'Looking for Node.js/Go, not Java background.'},

            # Neha applies to Data Analyst and ML jobs
            {'applicant': seekers[3], 'job': jobs[3], 'status': 'accepted',
             'cover_letter': 'I am a final year student with strong Python and SQL skills. I have built dashboards using Power BI for my college project.',
             'employer_note': 'Selected for internship. Joining date: June 1.'},
            {'applicant': seekers[3], 'job': jobs[7], 'status': 'pending',
             'cover_letter': 'I have completed my ML specialization and have deployed two fraud detection models in academic projects.',
             'employer_note': ''},

            # Karan applies to DevOps
            {'applicant': seekers[4], 'job': jobs[1], 'status': 'shortlisted',
             'cover_letter': 'DevOps is my passion. I manage Kubernetes clusters for 50+ microservices and have automated full CI/CD pipelines.',
             'employer_note': 'Very strong candidate.'},

            # Sneha applies to Flutter job
            {'applicant': seekers[5], 'job': jobs[5], 'status': 'pending',
             'cover_letter': 'I have 3 years of Flutter development and have published 2 apps on both Play Store and App Store.',
             'employer_note': ''},

            # Amit applies to Full Stack and Backend
            {'applicant': seekers[6], 'job': jobs[9], 'status': 'reviewed',
             'cover_letter': 'Node.js and MongoDB are my daily tools. I can contribute to the logistics tool from day one.',
             'employer_note': ''},
            {'applicant': seekers[6], 'job': jobs[6], 'status': 'pending',
             'cover_letter': 'I want to work in fintech and have built payment integrations with Razorpay and Stripe APIs before.',
             'employer_note': ''},

            # Divya applies to UI/UX
            {'applicant': seekers[7], 'job': jobs[8], 'status': 'shortlisted',
             'cover_letter': 'I have 3 years of UX design experience with Figma. My portfolio includes a food delivery app redesign with a 25% improvement in task completion rate.',
             'employer_note': 'Great portfolio. Call scheduled.'},
        ]

        for data in applications_data:
            Application.objects.create(**data)
            self.stdout.write(
                f'  📝 {data["applicant"].username} → {data["job"].title} [{data["status"]}]'
            )

        # -----------------------------------------------
        # SUMMARY
        # -----------------------------------------------
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Seed complete!'))
        self.stdout.write(f'   Employers  : {len(employers)}')
        self.stdout.write(f'   Job Seekers: {len(seekers)}')
        self.stdout.write(f'   Jobs       : {len(jobs)}')
        self.stdout.write(f'   Applications: {len(applications_data)}')
        self.stdout.write('')
        self.stdout.write('📋 Login credentials (all passwords: Test@1234)')
        self.stdout.write('   Employers  : hr@infosys.com, careers@tcs.com, jobs@flipkart.com, talent@razorpay.com, hr@zomato.com')
        self.stdout.write('   Job Seekers: arjun.sharma@careerstackmail.com, priya.mehta@careerstackmail.com, rahul.verma@careerstackmail.com ...')
