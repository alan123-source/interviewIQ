from app.services.resume_ai_service import analyze_resume


resume_text = """
ALAN PAUL JOHN
Software Engineer | Full Stack Developer

alanpauljohn385@gmail.com
9633022631
linkedin.com/in/alan-paul-john
github.com/alan123-source

PROFILE SUMMARY

Computer Science undergraduate graduating in 2027
with a strong foundation in Data Structures and Algorithms
and hands-on experience in full-stack web development using
React, Node.js, Express.js, and MongoDB.

SKILLS

Hard Skills:
JavaScript | Python | Embedded C | React | Node.js |
Express.js | MongoDB | SQL | REST APIs | Docker | Git/GitHub

Soft Skills:
Team Leadership | Communication | Problem Solving |
Time Management | Adaptability | Attention to Detail

PROJECTS

E-Commerce Platform with Personalized Product Recommendations

React, Node.js, Express.js, MongoDB, Stripe, Docker

Developed and deployed a full-stack MERN e-commerce platform
featuring authentication, shopping cart, wishlist, order
management, reviews, and an admin dashboard.

Implemented JWT-based authentication, coupon management,
product recommendations, Stripe payment integration,
and email notifications.

EDUCATION

Bachelor of Technology in Computer Science

College of Engineering Poonjar

2023 - Present

CGPA: 7.05
"""


result =analyze_resume(resume_text)

print(result)