"""Seed demo data into the SQLite database."""
import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models.teaching import Course, ClassModel, Student, Grade, Observation, Evaluation
from app.models.knowledge import TeachingModeTemplate, KnowledgeNode, KnowledgeEdge

DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")


def import_csv(db: Session, model, filepath: str, field_map: dict):
    df = pd.read_csv(filepath)
    count = 0
    for _, row in df.iterrows():
        kwargs = {}
        for csv_col, db_col in field_map.items():
            kwargs[db_col] = row[csv_col]
        db.add(model(**kwargs))
        count += 1
    db.commit()
    print(f"  Imported {count} rows into {model.__tablename__}")


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Course).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        print("Seeding database...")

        import_csv(db, Course, os.path.join(DATA_DIR, "courses.csv"), {
            "name": "name", "code": "code", "department": "department",
            "credits": "credits", "teacher_name": "teacher_name", "semester": "semester",
        })

        import_csv(db, ClassModel, os.path.join(DATA_DIR, "classes.csv"), {
            "name": "name", "course_id": "course_id", "semester": "semester",
            "student_count": "student_count",
        })

        import_csv(db, Student, os.path.join(DATA_DIR, "students.csv"), {
            "name": "name", "student_no": "student_no", "class_id": "class_id",
        })

        import_csv(db, Grade, os.path.join(DATA_DIR, "grades.csv"), {
            "student_id": "student_id", "class_id": "class_id", "exam_name": "exam_name",
            "score": "score", "knowledge_point": "knowledge_point", "max_score": "max_score",
        })

        import_csv(db, Observation, os.path.join(DATA_DIR, "observations.csv"), {
            "class_id": "class_id", "date": "date", "observer": "observer",
            "interaction_frequency": "interaction_frequency", "question_depth": "question_depth",
            "student_participation": "student_participation", "lecture_ratio": "lecture_ratio",
            "discussion_ratio": "discussion_ratio", "practice_ratio": "practice_ratio",
            "teaching_style_label": "teaching_style_label", "notes": "notes",
        })

        import_csv(db, Evaluation, os.path.join(DATA_DIR, "evaluations.csv"), {
            "class_id": "class_id", "semester": "semester", "dimension": "dimension",
            "score": "score",
        })

        print("Seeding complete!")

        # Seed mode templates and knowledge graph
        _seed_mode_templates(db)
        _seed_knowledge_graph(db)
        print("Extended seed data loaded!")

    finally:
        db.close()


def _seed_mode_templates(db: Session):
    if db.query(TeachingModeTemplate).count() > 0:
        return
    templates = [
        {"name": "翻转课堂", "category": "builtin", "description": "学生在课前通过视频/阅读自主学习新知识，课堂时间用于讨论、练习和深度互动。", "stages": [{"name": "课前自学", "duration": 30, "activity_type": "自学", "teacher_action": "提供学习资源", "student_action": "观看视频/阅读材料"}, {"name": "课前测验", "duration": 10, "activity_type": "测评", "teacher_action": "发布测验", "student_action": "完成在线测验"}, {"name": "课堂讨论", "duration": 20, "activity_type": "讨论", "teacher_action": "引导讨论", "student_action": "小组讨论"}, {"name": "深化练习", "duration": 25, "activity_type": "练习", "teacher_action": "针对性指导", "student_action": "完成进阶练习"}, {"name": "总结反馈", "duration": 5, "activity_type": "总结", "teacher_action": "点评总结", "student_action": "反思笔记"}], "suitable_scenarios": "概念性知识较多、学生自主学习能力较强的课程", "strengths": "提升课堂互动深度，培养学生自主学习能力", "limitations": "对学生自学能力和课前投入要求高"},
        {"name": "PBL项目式学习", "category": "builtin", "description": "以真实项目为驱动，学生在完成项目的过程中主动学习知识和技能。", "stages": [{"name": "项目启动", "duration": 20, "activity_type": "导入", "teacher_action": "发布项目任务", "student_action": "理解项目要求"}, {"name": "方案设计", "duration": 30, "activity_type": "设计", "teacher_action": "提供指导框架", "student_action": "小组设计方案"}, {"name": "实施开发", "duration": 60, "activity_type": "实践", "teacher_action": "巡回指导", "student_action": "分工协作实施"}, {"name": "成果展示", "duration": 25, "activity_type": "展示", "teacher_action": "组织评审", "student_action": "展示答辩"}, {"name": "反思总结", "duration": 15, "activity_type": "反思", "teacher_action": "点评反馈", "student_action": "撰写反思报告"}], "suitable_scenarios": "实践性强的专业课程，需要培养综合应用能力", "strengths": "培养解决问题能力、团队协作能力和自主学习能力", "limitations": "耗时较长，对教师项目设计能力要求高"},
        {"name": "BOPPPS教学法", "category": "builtin", "description": "六步结构化教学模式：导入(Bridge-in)→目标(Objective)→前测(Pre-assessment)→参与式学习(Participatory)→后测(Post-assessment)→总结(Summary)。", "stages": [{"name": "导入Bridge-in", "duration": 5, "activity_type": "导入", "teacher_action": "创设情境", "student_action": "进入学习状态"}, {"name": "目标Objective", "duration": 3, "activity_type": "讲解", "teacher_action": "明确学习目标", "student_action": "了解学习目标"}, {"name": "前测Pre-assessment", "duration": 7, "activity_type": "测评", "teacher_action": "快速检测", "student_action": "完成前测"}, {"name": "参与式学习", "duration": 25, "activity_type": "互动", "teacher_action": "组织互动活动", "student_action": "积极参与"}, {"name": "后测Post-assessment", "duration": 7, "activity_type": "测评", "teacher_action": "检测效果", "student_action": "完成后测"}, {"name": "总结Summary", "duration": 3, "activity_type": "总结", "teacher_action": "总结要点", "student_action": "整理笔记"}], "suitable_scenarios": "各类课程通用，尤其适合需要明确教学目标的课程", "strengths": "结构清晰，目标明确，便于评估教学效果", "limitations": "时间控制要求严格，灵活性相对不足"},
        {"name": "对分课堂", "category": "builtin", "description": "一半时间教师讲授，一半时间学生讨论，强调讲授与讨论的有机结合。", "stages": [{"name": "教师讲授", "duration": 25, "activity_type": "讲授", "teacher_action": "精讲核心内容", "student_action": "听讲记笔记"}, {"name": "独立思考", "duration": 5, "activity_type": "思考", "teacher_action": "提出思考题", "student_action": "独立完成作业"}, {"name": "小组讨论", "duration": 12, "activity_type": "讨论", "teacher_action": "巡视观察", "student_action": "组内讨论交流"}, {"name": "全班交流", "duration": 8, "activity_type": "展示", "teacher_action": "组织全班交流", "student_action": "代表发言"}], "suitable_scenarios": "理论性较强的课程，班级规模适中", "strengths": "平衡讲授与互动，操作简单易推广", "limitations": "对讨论题设计质量要求高"},
        {"name": "5E教学法", "category": "builtin", "description": "基于建构主义的五步教学：参与(Engage)→探究(Explore)→解释(Explain)→拓展(Elaborate)→评价(Evaluate)。", "stages": [{"name": "参与Engage", "duration": 8, "activity_type": "导入", "teacher_action": "激发兴趣", "student_action": "产生好奇心"}, {"name": "探究Explore", "duration": 20, "activity_type": "探究", "teacher_action": "提供探究材料", "student_action": "动手探究"}, {"name": "解释Explain", "duration": 12, "activity_type": "讲解", "teacher_action": "引导解释", "student_action": "表达理解"}, {"name": "拓展Elaborate", "duration": 15, "activity_type": "应用", "teacher_action": "提供拓展任务", "student_action": "应用新知识"}, {"name": "评价Evaluate", "duration": 5, "activity_type": "评价", "teacher_action": "多元评价", "student_action": "自评互评"}], "suitable_scenarios": "科学、工程类课程，需要探究和实验", "strengths": "符合认知规律，学生参与度高", "limitations": "准备探究材料工作量大"},
        {"name": "案例教学法", "category": "builtin", "description": "以真实案例为载体，通过分析、讨论、决策培养学生的分析能力和判断力。", "stages": [{"name": "案例呈现", "duration": 10, "activity_type": "导入", "teacher_action": "呈现案例", "student_action": "阅读案例"}, {"name": "个人分析", "duration": 10, "activity_type": "思考", "teacher_action": "提出分析框架", "student_action": "独立分析"}, {"name": "小组研讨", "duration": 15, "activity_type": "讨论", "teacher_action": "引导讨论方向", "student_action": "小组研讨"}, {"name": "全班交流", "duration": 12, "activity_type": "展示", "teacher_action": "点评总结", "student_action": "分享观点"}, {"name": "理论升华", "duration": 3, "activity_type": "总结", "teacher_action": "归纳理论", "student_action": "记录要点"}], "suitable_scenarios": "管理类、法律类、医学类等需要决策能力的课程", "strengths": "贴近实际，培养分析决策能力", "limitations": "优质案例库建设成本高"},
        {"name": "混合式教学", "category": "builtin", "description": "线上学习与线下课堂相结合，利用技术手段优化教学效果。", "stages": [{"name": "线上预习", "duration": 25, "activity_type": "线上", "teacher_action": "发布线上资源", "student_action": "线上自学"}, {"name": "线下精讲", "duration": 20, "activity_type": "讲授", "teacher_action": "精讲难点", "student_action": "听讲提问"}, {"name": "互动研讨", "duration": 15, "activity_type": "讨论", "teacher_action": "组织讨论", "student_action": "互动交流"}, {"name": "线上巩固", "duration": 20, "activity_type": "线上", "teacher_action": "推送练习", "student_action": "在线练习"}, {"name": "反馈调整", "duration": 10, "activity_type": "反馈", "teacher_action": "分析数据", "student_action": "查看反馈"}], "suitable_scenarios": "信息技术条件较好的课程，适合大规模教学", "strengths": "灵活高效，数据可追踪", "limitations": "依赖技术平台，学生需具备在线学习习惯"},
        {"name": "探究式学习", "category": "builtin", "description": "以问题为导向，学生通过自主探究和实验发现知识。", "stages": [{"name": "提出问题", "duration": 5, "activity_type": "导入", "teacher_action": "提出驱动问题", "student_action": "明确探究问题"}, {"name": "猜想假设", "duration": 8, "activity_type": "思考", "teacher_action": "引导思考", "student_action": "提出假设"}, {"name": "设计实验", "duration": 10, "activity_type": "设计", "teacher_action": "提供资源", "student_action": "设计探究方案"}, {"name": "实施探究", "duration": 20, "activity_type": "实践", "teacher_action": "巡回指导", "student_action": "动手实验"}, {"name": "得出结论", "duration": 7, "activity_type": "总结", "teacher_action": "组织交流", "student_action": "汇报结论"}], "suitable_scenarios": "自然科学、工程技术类实验课程", "strengths": "培养科学思维和探究能力", "limitations": "实验条件要求高，课时消耗大"},
        {"name": "讲授+练习式", "category": "builtin", "description": "传统高效模式：教师精讲核心知识，学生通过大量练习巩固。", "stages": [{"name": "导入复习", "duration": 3, "activity_type": "导入", "teacher_action": "复习旧知", "student_action": "回顾"}, {"name": "新知讲授", "duration": 20, "activity_type": "讲授", "teacher_action": "系统讲授", "student_action": "听讲记录"}, {"name": "例题示范", "duration": 8, "activity_type": "示范", "teacher_action": "展示解题", "student_action": "观察理解"}, {"name": "独立练习", "duration": 15, "activity_type": "练习", "teacher_action": "巡视辅导", "student_action": "独立练习"}, {"name": "讲评纠错", "duration": 4, "activity_type": "反馈", "teacher_action": "讲评典型错误", "student_action": "订正"}], "suitable_scenarios": "数学、编程等技能型课程的基础阶段", "strengths": "效率高，知识传递快", "limitations": "学生被动接受，高阶思维培养不足"},
        {"name": "同伴教学法", "category": "builtin", "description": "教师提出概念性问题，学生先独立思考作答，再与同伴讨论修正答案。", "stages": [{"name": "概念讲授", "duration": 12, "activity_type": "讲授", "teacher_action": "简短讲授", "student_action": "听讲"}, {"name": "概念测试", "duration": 3, "activity_type": "测评", "teacher_action": "发布选择题", "student_action": "独立作答"}, {"name": "同伴讨论", "duration": 5, "activity_type": "讨论", "teacher_action": "观察讨论", "student_action": "与同伴讨论"}, {"name": "二次作答", "duration": 2, "activity_type": "测评", "teacher_action": "再次收集答案", "student_action": "修正答案"}, {"name": "全班讲解", "duration": 8, "activity_type": "讲解", "teacher_action": "讲解正确答案", "student_action": "理解巩固"}], "suitable_scenarios": "概念理解类课程，大班教学", "strengths": "即时反馈，促进概念理解", "limitations": "需设计高质量概念测试题"},
        {"name": "游戏化教学", "category": "builtin", "description": "将游戏元素和机制融入教学过程，提升学习动机和参与度。", "stages": [{"name": "规则说明", "duration": 5, "activity_type": "讲解", "teacher_action": "说明游戏规则", "student_action": "理解规则"}, {"name": "分组准备", "duration": 3, "activity_type": "组织", "teacher_action": "分组", "student_action": "团队准备"}, {"name": "游戏挑战", "duration": 25, "activity_type": "实践", "teacher_action": "主持游戏", "student_action": "参与挑战"}, {"name": "计分排名", "duration": 3, "activity_type": "评价", "teacher_action": "公布结果", "student_action": "查看排名"}, {"name": "知识复盘", "duration": 4, "activity_type": "总结", "teacher_action": "总结知识点", "student_action": "巩固知识"}], "suitable_scenarios": "需要提升学习兴趣的课程，适合年轻学生", "strengths": "趣味性强，参与度高", "limitations": "游戏设计与教学目标结合有难度"},
        {"name": "研讨式教学", "category": "builtin", "description": "以学术研讨为主要形式，教师引导，学生围绕主题进行深入讨论。", "stages": [{"name": "主题发布", "duration": 5, "activity_type": "导入", "teacher_action": "发布研讨主题", "student_action": "了解主题"}, {"name": "文献研读", "duration": 15, "activity_type": "阅读", "teacher_action": "提供文献", "student_action": "研读文献"}, {"name": "分组研讨", "duration": 15, "activity_type": "讨论", "teacher_action": "巡回参与", "student_action": "深入研讨"}, {"name": "汇报交流", "duration": 12, "activity_type": "展示", "teacher_action": "主持交流", "student_action": "汇报观点"}, {"name": "总结深化", "duration": 3, "activity_type": "总结", "teacher_action": "提炼升华", "student_action": "撰写心得"}], "suitable_scenarios": "研究生课程、高年级专业选修课", "strengths": "培养批判性思维和学术表达能力", "limitations": "对学生的知识储备要求高"},
    ]
    for t in templates:
        db.add(TeachingModeTemplate(**t))
    db.commit()
    print(f"  Seeded {len(templates)} teaching mode templates")


def _seed_knowledge_graph(db: Session):
    if db.query(KnowledgeNode).count() > 0:
        return
    # Data Structures course knowledge graph
    nodes = [
        {"name": "线性表", "course_id": 1, "parent_id": None, "difficulty": 2.0, "order_index": 1},
        {"name": "顺序表", "course_id": 1, "parent_id": 1, "difficulty": 2.0, "order_index": 1},
        {"name": "链表", "course_id": 1, "parent_id": 1, "difficulty": 2.5, "order_index": 2},
        {"name": "栈和队列", "course_id": 1, "parent_id": None, "difficulty": 2.5, "order_index": 2},
        {"name": "栈", "course_id": 1, "parent_id": 4, "difficulty": 2.0, "order_index": 1},
        {"name": "队列", "course_id": 1, "parent_id": 4, "difficulty": 2.5, "order_index": 2},
        {"name": "树与二叉树", "course_id": 1, "parent_id": None, "difficulty": 3.5, "order_index": 3},
        {"name": "二叉树遍历", "course_id": 1, "parent_id": 7, "difficulty": 3.5, "order_index": 1},
        {"name": "二叉搜索树", "course_id": 1, "parent_id": 7, "difficulty": 4.0, "order_index": 2},
        {"name": "图算法", "course_id": 1, "parent_id": None, "difficulty": 4.5, "order_index": 4},
        {"name": "图的遍历", "course_id": 1, "parent_id": 10, "difficulty": 4.0, "order_index": 1},
        {"name": "最短路径", "course_id": 1, "parent_id": 10, "difficulty": 4.5, "order_index": 2},
        {"name": "排序算法", "course_id": 1, "parent_id": None, "difficulty": 3.0, "order_index": 5},
        {"name": "简单排序", "course_id": 1, "parent_id": 13, "difficulty": 2.5, "order_index": 1},
        {"name": "高级排序", "course_id": 1, "parent_id": 13, "difficulty": 3.5, "order_index": 2},
    ]
    node_map = {}
    for n in nodes:
        obj = KnowledgeNode(**n)
        db.add(obj)
        db.flush()
        node_map[n["name"]] = obj.id

    edges = [
        ("顺序表", "链表", "parallel"),
        ("线性表", "栈和队列", "prerequisite"),
        ("线性表", "树与二叉树", "prerequisite"),
        ("栈和队列", "树与二叉树", "prerequisite"),
        ("链表", "二叉树遍历", "prerequisite"),
        ("二叉树遍历", "二叉搜索树", "prerequisite"),
        ("树与二叉树", "图算法", "prerequisite"),
        ("图的遍历", "最短路径", "prerequisite"),
        ("线性表", "排序算法", "prerequisite"),
        ("简单排序", "高级排序", "prerequisite"),
    ]
    for src, tgt, rel in edges:
        if src in node_map and tgt in node_map:
            db.add(KnowledgeEdge(source_id=node_map[src], target_id=node_map[tgt], relation_type=rel))
    db.commit()
    print(f"  Seeded {len(nodes)} knowledge nodes + {len(edges)} edges")


if __name__ == "__main__":
    seed()
