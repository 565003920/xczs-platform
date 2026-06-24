"""
Full-flow demo data generator for v2.0 closed loop.
Generates all entities programmatically with realistic, varied patterns.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.teaching import Course, ClassModel, Student, Grade, Observation, Evaluation
from app.models.knowledge import TeachingModeTemplate, KnowledgeNode, KnowledgeEdge
from app.models.audit import AuditLog, Notification

random.seed(42)

# ── data definitions ──

COURSES = [
    {"name": "数据结构", "code": "CS201", "department": "计算机学院", "credits": 4.0, "teacher_name": "张教授", "semester": "2024-2025-1"},
    {"name": "操作系统", "code": "CS302", "department": "计算机学院", "credits": 3.5, "teacher_name": "李副教授", "semester": "2024-2025-1"},
    {"name": "计算机网络", "code": "CS305", "department": "计算机学院", "credits": 3.0, "teacher_name": "王教授", "semester": "2024-2025-1"},
    {"name": "软件工程", "code": "SE401", "department": "计算机学院", "credits": 3.0, "teacher_name": "赵副教授", "semester": "2024-2025-1"},
    {"name": "数据库原理", "code": "CS210", "department": "计算机学院", "credits": 3.5, "teacher_name": "钱教授", "semester": "2024-2025-1"},
    {"name": "人工智能导论", "code": "AI101", "department": "人工智能学院", "credits": 3.0, "teacher_name": "孙副教授", "semester": "2024-2025-1"},
]

CLASSES = [
    # course_id, name, semester, semester_index, student_count
    (1, "2024级软件工程1班", "2024-2025-1", 1, 12),
    (1, "2024级软件工程2班", "2024-2025-1", 1, 12),
    (2, "2024级计算机科学1班", "2024-2025-1", 1, 12),
    (2, "2024级计算机科学2班", "2024-2025-1", 1, 12),
    (3, "2024级网工1班", "2024-2025-1", 1, 12),
    (3, "2024级网工2班", "2024-2025-1", 1, 12),
    (4, "2024级软工3班", "2024-2025-1", 1, 12),
    (4, "2024级软工4班", "2024-2025-1", 1, 12),
    (5, "2024级数科1班", "2024-2025-1", 1, 12),
    (5, "2024级数科2班", "2024-2025-1", 1, 12),
    (6, "2024级AI实验班", "2024-2025-1", 1, 12),
    (6, "2024级AI普通班", "2024-2025-1", 1, 12),
    # 跨课程班级（同一班级名，不同课程）
    (2, "2024级软件工程1班", "2024-2025-1", 1, 12),
    (4, "2024级软件工程1班", "2024-2025-1", 1, 12),
    (3, "2024级软件工程2班", "2024-2025-1", 1, 12),
    (1, "2024级计算机科学1班", "2024-2025-1", 1, 12),
    (5, "2024级AI实验班", "2024-2025-1", 1, 12),
]

SURNAMES = ["张","李","王","赵","钱","孙","周","吴","郑","冯","陈","林","黄","刘","杨","许","何","吕","施","马","朱","秦","尤","曹","严","华","金","魏","陶","姜","戚","谢","邹","柏","水","窦","章","云","苏","潘","葛","奚","范","彭","郎","鲁","韦","昌","苗","凤","花","方","俞","任","袁","柳","鲍","史","唐","费","廉","岑","薛","雷","贺","倪","汤","滕","殷","罗","毕","郝","邬","安","常","乐","于","时","傅","皮","卞","齐","康","伍","余","元","卜","顾","孟","平","黄","和","穆","萧","尹","姚","邵","湛","汪","祁","毛","禹","狄","米","贝","明","臧","计","伏","成","戴","谈","宋","茅","庞","熊","纪","舒","屈","项","祝","董","梁","杜","阮","蓝","闵","席","季","麻","强","贾","路","娄","危","江","童","颜","郭","梅","盛","林","刁","钟","徐","邱","骆","高","夏","蔡","田","樊","胡","凌","霍","虞","万","支","柯","昝","管","卢","莫","经","房","裘","缪","干","解","应","宗","丁","宣","贲","邓","郁","单","杭","洪","包","诸","左","石","崔","吉","钮","龚","程","嵇","邢","滑","裴","陆","荣","翁","荀","羊","於","惠","甄","麴","家","封","芮","羿","储","靳","汲","邴","糜","松","井","段","富","巫","乌","焦","巴","弓","牧","隗","山","谷","车","侯","宓","蓬","全","郗","班","仰","秋","仲","伊","宫","宁","仇","栾","暴","甘","钭","厉","戎","祖","武","符","刘","景","詹","束","龙","叶","幸","司","韶","郜","黎","蓟","薄","印","宿","白","怀","蒲","邰","从","鄂","索","咸","籍","赖","卓","蔺","屠","蒙","池","乔","阴","鬱","胥","能","苍","双","闻","莘","党","翟","谭","贡","劳","逄","姬","申","扶","堵","冉","宰","郦","雍","卻","璩","桑","桂","濮","牛","寿","通","边","扈","燕","冀","郏","浦","尚","农","温","别","庄","晏","柴","瞿","阎","充","慕","连","茹","习","宦","艾","鱼","容","向","古","易","慎","戈","廖","庾","终","暨","居","衡","步","都","耿","满","弘","匡","国","文","寇","广","禄","阙","东","欧","殳","沃","利","蔚","越","夔","隆","师","巩","厍","聂","晁","勾","敖","融","冷","訾","辛","阚","那","简","饶","空","曾","毋","沙","乜","养","鞠","须","丰","巢","关","蒯","相","查","後","荆","红","游","竺","权","逯","盖","益","桓","公","万俟","司马","上官","欧阳","夏侯","诸葛","闻人","东方","赫连","皇甫","尉迟","公羊","澹台","公冶","宗政","濮阳","淳于","单于","太叔","申屠","公孙","仲孙","轩辕","令狐","钟离","宇文","长孙","慕容","鲜于","闾丘","司徒","司空","丌官","司寇","仉","督","子车","颛孙","端木","巫马","公西","漆雕","乐正","壤驷","公良","拓跋","夹谷","宰父","谷梁","晋","楚","闫","法","汝","鄢","涂","钦","段干","百里","东郭","南门","呼延","归","海","羊舌","微生","岳","帅","缑","亢","况","後","有","琴","梁丘","左丘","东门","西门","商","牟","佘","佴","伯","赏","南宫","墨","哈","谯","笪","年","爱","阳","佟","第五","言","福"]

KP_MAP = {
    1: ["线性表","顺序表","链表","栈和队列","栈","队列","树与二叉树","二叉树遍历","二叉搜索树","图算法","图的遍历","最短路径","排序算法","简单排序","高级排序"],
    2: ["进程管理","内存管理","文件系统","设备管理","死锁","调度算法","虚拟内存","I/O系统","并发编程","同步互斥"],
    3: ["OSI模型","TCP/IP","IP地址","路由算法","传输层","应用层协议","网络安全","网络拓扑","子网划分","DNS"],
    4: ["需求分析","系统设计","软件测试","敏捷开发","UML建模","设计模式","代码重构","项目管理","版本控制","持续集成"],
    5: ["关系模型","SQL查询","范式设计","事务管理","索引优化","存储过程","并发控制","数据备份","NoSQL","数据仓库"],
    6: ["搜索算法","知识表示","机器学习","神经网络","自然语言处理","计算机视觉","强化学习","专家系统","遗传算法","深度学习"],
}

MODE_TEMPLATES = [
    {"name": "翻转课堂", "category": "builtin", "description": "学生课前自学，课堂用于讨论和深度互动", "stages": [{"name":"课前自学","duration":30,"activity_type":"自学","teacher_action":"提供学习资源","student_action":"观看视频/阅读"},{"name":"课前测验","duration":10,"activity_type":"测评","teacher_action":"发布测验","student_action":"完成测验"},{"name":"课堂讨论","duration":20,"activity_type":"讨论","teacher_action":"引导讨论","student_action":"小组讨论"},{"name":"深化练习","duration":25,"activity_type":"练习","teacher_action":"针对性指导","student_action":"进阶练习"},{"name":"总结反馈","duration":5,"activity_type":"总结","teacher_action":"点评总结","student_action":"反思笔记"}], "suitable_scenarios": "概念性知识较多、学生自主学习能力较强的课程", "strengths": "提升课堂互动深度", "limitations": "对学生自学能力要求高"},
    {"name": "PBL项目式学习", "category": "builtin", "description": "以真实项目驱动，学生主动学习知识和技能", "stages": [{"name":"项目启动","duration":20,"activity_type":"导入","teacher_action":"发布项目任务","student_action":"理解要求"},{"name":"方案设计","duration":30,"activity_type":"设计","teacher_action":"提供指导","student_action":"设计方案"},{"name":"实施开发","duration":60,"activity_type":"实践","teacher_action":"巡回指导","student_action":"分工实施"},{"name":"成果展示","duration":25,"activity_type":"展示","teacher_action":"组织评审","student_action":"展示答辩"},{"name":"反思总结","duration":15,"activity_type":"反思","teacher_action":"点评反馈","student_action":"撰写报告"}], "suitable_scenarios": "实践性强的课程", "strengths": "培养解决问题和团队协作能力", "limitations": "耗时较长"},
    {"name": "BOPPPS教学法", "category": "builtin", "description": "六步结构化教学", "stages": [{"name":"导入","duration":5,"activity_type":"导入","teacher_action":"创设情境","student_action":"进入状态"},{"name":"目标","duration":3,"activity_type":"讲解","teacher_action":"明确目标","student_action":"了解目标"},{"name":"前测","duration":7,"activity_type":"测评","teacher_action":"快速检测","student_action":"完成前测"},{"name":"参与式学习","duration":25,"activity_type":"互动","teacher_action":"组织活动","student_action":"积极参与"},{"name":"后测","duration":7,"activity_type":"测评","teacher_action":"检测效果","student_action":"完成后测"},{"name":"总结","duration":3,"activity_type":"总结","teacher_action":"总结要点","student_action":"整理笔记"}], "suitable_scenarios": "通用", "strengths": "结构清晰", "limitations": "时间控制严格"},
    {"name": "对分课堂", "category": "builtin", "description": "一半讲授，一半讨论", "stages": [{"name":"教师讲授","duration":25,"activity_type":"讲授","teacher_action":"精讲核心","student_action":"听讲笔记"},{"name":"独立思考","duration":5,"activity_type":"思考","teacher_action":"提出思考题","student_action":"独立完成"},{"name":"小组讨论","duration":12,"activity_type":"讨论","teacher_action":"巡视观察","student_action":"组内讨论"},{"name":"全班交流","duration":8,"activity_type":"展示","teacher_action":"组织交流","student_action":"代表发言"}], "suitable_scenarios": "理论性较强的课程", "strengths": "平衡讲授与互动", "limitations": "讨论题质量要求高"},
    {"name": "5E教学法", "category": "builtin", "description": "参与-探究-解释-拓展-评价", "stages": [{"name":"参与","duration":8,"activity_type":"导入","teacher_action":"激发兴趣","student_action":"产生好奇"},{"name":"探究","duration":20,"activity_type":"探究","teacher_action":"提供材料","student_action":"动手探究"},{"name":"解释","duration":12,"activity_type":"讲解","teacher_action":"引导解释","student_action":"表达理解"},{"name":"拓展","duration":15,"activity_type":"应用","teacher_action":"提供任务","student_action":"应用新知"},{"name":"评价","duration":5,"activity_type":"评价","teacher_action":"多元评价","student_action":"自评互评"}], "suitable_scenarios": "科学工程类", "strengths": "符合认知规律", "limitations": "准备材料工作量大"},
    {"name": "案例教学法", "category": "builtin", "description": "以真实案例分析驱动教学", "stages": [{"name":"案例呈现","duration":10,"activity_type":"导入","teacher_action":"呈现案例","student_action":"阅读案例"},{"name":"个人分析","duration":10,"activity_type":"思考","teacher_action":"提供框架","student_action":"独立分析"},{"name":"小组研讨","duration":15,"activity_type":"讨论","teacher_action":"引导方向","student_action":"小组研讨"},{"name":"全班交流","duration":12,"activity_type":"展示","teacher_action":"点评总结","student_action":"分享观点"},{"name":"理论升华","duration":3,"activity_type":"总结","teacher_action":"归纳理论","student_action":"记录要点"}], "suitable_scenarios": "管理法律医学类", "strengths": "贴近实际", "limitations": "优质案例库建设成本高"},
    {"name": "混合式教学", "category": "builtin", "description": "线上线下相结合", "stages": [{"name":"线上预习","duration":25,"activity_type":"线上","teacher_action":"发布资源","student_action":"线上自学"},{"name":"线下精讲","duration":20,"activity_type":"讲授","teacher_action":"精讲难点","student_action":"听讲提问"},{"name":"互动研讨","duration":15,"activity_type":"讨论","teacher_action":"组织讨论","student_action":"互动交流"},{"name":"线上巩固","duration":20,"activity_type":"线上","teacher_action":"推送练习","student_action":"在线练习"},{"name":"反馈调整","duration":10,"activity_type":"反馈","teacher_action":"分析数据","student_action":"查看反馈"}], "suitable_scenarios": "信息技术条件好的课程", "strengths": "灵活高效", "limitations": "依赖技术平台"},
    {"name": "探究式学习", "category": "builtin", "description": "以问题为导向自主探究", "stages": [{"name":"提出问题","duration":5,"activity_type":"导入","teacher_action":"提出驱动问题","student_action":"明确问题"},{"name":"猜想假设","duration":8,"activity_type":"思考","teacher_action":"引导思考","student_action":"提出假设"},{"name":"设计实验","duration":10,"activity_type":"设计","teacher_action":"提供资源","student_action":"设计方案"},{"name":"实施探究","duration":20,"activity_type":"实践","teacher_action":"巡回指导","student_action":"动手实验"},{"name":"得出结论","duration":7,"activity_type":"总结","teacher_action":"组织交流","student_action":"汇报结论"}], "suitable_scenarios": "自然科学实验类", "strengths": "培养科学思维", "limitations": "实验条件要求高"},
    {"name": "讲授+练习式", "category": "builtin", "description": "传统高效模式", "stages": [{"name":"导入复习","duration":3,"activity_type":"导入","teacher_action":"复习旧知","student_action":"回顾"},{"name":"新知讲授","duration":20,"activity_type":"讲授","teacher_action":"系统讲授","student_action":"听讲记录"},{"name":"例题示范","duration":8,"activity_type":"示范","teacher_action":"展示解题","student_action":"观察理解"},{"name":"独立练习","duration":15,"activity_type":"练习","teacher_action":"巡视辅导","student_action":"独立练习"},{"name":"讲评纠错","duration":4,"activity_type":"反馈","teacher_action":"讲评错误","student_action":"订正"}], "suitable_scenarios": "数学编程等技能型基础阶段", "strengths": "效率高", "limitations": "高阶思维培养不足"},
    {"name": "同伴教学法", "category": "builtin", "description": "概念测试+同伴讨论", "stages": [{"name":"概念讲授","duration":12,"activity_type":"讲授","teacher_action":"简短讲授","student_action":"听讲"},{"name":"概念测试","duration":3,"activity_type":"测评","teacher_action":"发布选择题","student_action":"独立作答"},{"name":"同伴讨论","duration":5,"activity_type":"讨论","teacher_action":"观察讨论","student_action":"同伴讨论"},{"name":"二次作答","duration":2,"activity_type":"测评","teacher_action":"收集答案","student_action":"修正答案"},{"name":"全班讲解","duration":8,"activity_type":"讲解","teacher_action":"讲解答案","student_action":"理解巩固"}], "suitable_scenarios": "概念理解类大班教学", "strengths": "即时反馈", "limitations": "需设计高质量测试题"},
    {"name": "游戏化教学", "category": "builtin", "description": "游戏元素融入教学", "stages": [{"name":"规则说明","duration":5,"activity_type":"讲解","teacher_action":"说明规则","student_action":"理解规则"},{"name":"分组准备","duration":3,"activity_type":"组织","teacher_action":"分组","student_action":"团队准备"},{"name":"游戏挑战","duration":25,"activity_type":"实践","teacher_action":"主持游戏","student_action":"参与挑战"},{"name":"计分排名","duration":3,"activity_type":"评价","teacher_action":"公布结果","student_action":"查看排名"},{"name":"知识复盘","duration":4,"activity_type":"总结","teacher_action":"总结知识","student_action":"巩固知识"}], "suitable_scenarios": "需提升兴趣的课程", "strengths": "趣味性强", "limitations": "与教学目标结合有难度"},
    {"name": "研讨式教学", "category": "builtin", "description": "学术研讨形式深入讨论", "stages": [{"name":"主题发布","duration":5,"activity_type":"导入","teacher_action":"发布主题","student_action":"了解主题"},{"name":"文献研读","duration":15,"activity_type":"阅读","teacher_action":"提供文献","student_action":"研读文献"},{"name":"分组研讨","duration":15,"activity_type":"讨论","teacher_action":"巡回参与","student_action":"深入研讨"},{"name":"汇报交流","duration":12,"activity_type":"展示","teacher_action":"主持交流","student_action":"汇报观点"},{"name":"总结深化","duration":3,"activity_type":"总结","teacher_action":"提炼升华","student_action":"撰写心得"}], "suitable_scenarios": "研究生高年级课程", "strengths": "培养批判性思维", "limitations": "知识储备要求高"},
]

# ── Knowledge graph edges for course 1 (data structures) ──
KG_EDGES = [
    (1, 2, "contains"), (1, 3, "contains"),
    (2, 3, "parallel"),
    (4, 5, "contains"), (4, 6, "contains"),
    (7, 8, "contains"), (7, 9, "contains"),
    (8, 9, "prerequisite"),
    (10, 11, "contains"), (10, 12, "contains"),
    (11, 12, "prerequisite"),
    (13, 14, "contains"), (13, 15, "contains"),
    (14, 15, "prerequisite"),
    (1, 4, "prerequisite"), (4, 7, "prerequisite"),
    (3, 8, "prerequisite"), (7, 10, "prerequisite"),
    (1, 13, "prerequisite"),
]

KG_DIFFICULTY = [2.0, 2.0, 2.5, 2.5, 2.0, 2.5, 3.5, 3.5, 4.0, 4.5, 4.0, 4.5, 3.0, 2.5, 3.5]

# ── generation helpers ──

def gen_student_name(i: int) -> str:
    return f"{SURNAMES[i % len(SURNAMES)]}{'一二三四五六七八九十'[i % 10]}"

def gen_student_no(class_idx: int, i: int) -> str:
    return f"2024{class_idx+1:03d}{i+1:02d}"

# Each class has a "personality" dict that controls grade distribution
CLASS_PERSONALITIES = {
    # Excellent: high scores, high participation
    1: {"base": 78, "sigma": 10, "participation": 4},
    # Good: above average, good participation, practice-heavy
    2: {"base": 82, "sigma": 8, "participation": 5},
    # Average: medium, traditional lecture
    3: {"base": 68, "sigma": 14, "participation": 3},
    # Struggling: below average
    4: {"base": 58, "sigma": 16, "participation": 2},
    # Improving: moderate, improving trend
    5: {"base": 70, "sigma": 12, "participation": 3},
    # Good but exam-heavy
    6: {"base": 75, "sigma": 10, "participation": 4},
    # Excellent, very interactive
    7: {"base": 80, "sigma": 9, "participation": 4},
    # Below average, needs improvement
    8: {"base": 62, "sigma": 15, "participation": 3},
    # Strong, good at practice
    9: {"base": 76, "sigma": 11, "participation": 4},
    # Struggling, low motivation
    10: {"base": 55, "sigma": 17, "participation": 2},
    # Elite, high participation
    11: {"base": 88, "sigma": 6, "participation": 5},
    # Average, lecture-heavy
    12: {"base": 65, "sigma": 14, "participation": 3},
    # Cross-course classes
    13: {"base": 72, "sigma": 10, "participation": 3},   # 软件工程1班-操作系统
    14: {"base": 75, "sigma": 9, "participation": 4},     # 软件工程1班-软件工程
    15: {"base": 78, "sigma": 8, "participation": 4},     # 软件工程2班-计算机网络
    16: {"base": 70, "sigma": 11, "participation": 3},    # 计算机科学1班-数据结构
    17: {"base": 85, "sigma": 7, "participation": 5},     # AI实验班-数据库
}


def seed(db: Session):
    print("=== 学程智枢 v2.0 全流程测试数据生成 ===")

    # ── 1. Courses ──
    course_ids = []
    for c in COURSES:
        obj = Course(**c)
        db.add(obj)
        db.flush()
        course_ids.append(obj.id)
    db.commit()
    print(f"✅ 课程: {len(course_ids)}")

    # ── 2. Classes ──
    class_ids = []
    for course_id, name, semester, si, sc in CLASSES:
        obj = ClassModel(name=name, course_id=course_id, semester=semester, semester_index=si, student_count=sc)
        db.add(obj)
        db.flush()
        class_ids.append(obj.id)
    db.commit()
    print(f"✅ 班级: {len(class_ids)}")

    # ── 3. Students ──
    student_ids_by_class = {}
    for ci, (_, _, _, _, count) in enumerate(CLASSES):
        class_id = class_ids[ci]
        sids = []
        for i in range(count):
            obj = Student(name=gen_student_name(ci * 20 + i), student_no=gen_student_no(ci, i), class_id=class_id)
            db.add(obj)
            db.flush()
            sids.append(obj.id)
        student_ids_by_class[class_id] = sids
    db.commit()
    total_students = sum(len(v) for v in student_ids_by_class.values())
    print(f"✅ 学生: {total_students}")

    # ── 4. Grades ──
    grade_count = 0
    for ci, (course_id, _, _, si, count) in enumerate(CLASSES):
        class_id = class_ids[ci]
        kps = KP_MAP.get(course_id, ["基础知识","进阶知识"])
        personality = CLASS_PERSONALITIES.get(class_id, {"base": 70, "sigma": 15})
        for sid in student_ids_by_class[class_id]:
            # Generate 2-4 exam records per student
            exam_names = ["期中考试", "期末考试", "单元测验", "课堂小测"]
            for exam_i in range(random.randint(2, 4)):
                kp = random.choice(kps)
                score = max(0, min(100, round(random.gauss(personality["base"], personality["sigma"]))))
                # Make later exams slightly better (improvement trend)
                score = min(100, score + exam_i * random.randint(0, 3))
                db.add(Grade(student_id=sid, class_id=class_id, exam_name=exam_names[exam_i],
                            score=score, knowledge_point=kp, max_score=100.0))
                grade_count += 1
    db.commit()
    print(f"✅ 成绩记录: {grade_count}")

    # ── 5. Observations ──
    obs_count = 0
    mode_labels = ["混合型(讲授+互动)", "讲授主导型", "互动讨论型", "实践驱动型"]
    for ci, (course_id, _, _, si, count) in enumerate(CLASSES):
        class_id = class_ids[ci]
        personality = CLASS_PERSONALITIES.get(class_id, {"participation": 3})
        p = personality["participation"]
        # 2-4 observations per class
        for oi in range(random.randint(2, 4)):
            inter_freq = max(1, min(5, p + random.randint(-1, 1)))
            q_depth = max(1, min(5, p + random.randint(-1, 0)))
            stu_part = max(1, min(5, p))
            # Determine mode based on lecture/practice ratio
            if ci % 4 == 0:
                label, lec, disc, prac = "互动讨论型", 0.30, 0.40, 0.30
            elif ci % 4 == 1:
                label, lec, disc, prac = "实践驱动型", 0.25, 0.25, 0.50
            elif ci % 4 == 2:
                label, lec, disc, prac = "讲授主导型", 0.65, 0.20, 0.15
            else:
                label, lec, disc, prac = "混合型(讲授+互动)", 0.45, 0.30, 0.25
            db.add(Observation(class_id=class_id, date=f"2024-{9+oi:02d}-{10+oi*5:02d}",
                               observer=random.choice(["张督导","李督导","王督导"]),
                               interaction_frequency=inter_freq, question_depth=q_depth,
                               student_participation=stu_part, lecture_ratio=lec,
                               discussion_ratio=disc, practice_ratio=prac,
                               teaching_style_label=label, notes=""))
            obs_count += 1
    db.commit()
    print(f"✅ 课堂观察: {obs_count}")

    # ── 6. Evaluations ──
    eval_count = 0
    dims = ["teaching_attitude", "content_depth", "method_appropriateness", "interaction_quality", "overall_satisfaction"]
    for ci, (_, _, _, _, _) in enumerate(CLASSES):
        class_id = class_ids[ci]
        personality = CLASS_PERSONALITIES.get(class_id, {"base": 70, "participation": 3})
        base_score = personality["base"] + 10  # evaluation tends slightly higher
        for dim in dims:
            score = max(30, min(100, round(random.gauss(base_score, 8))))
            db.add(Evaluation(class_id=class_id, semester="2024-2025-1", dimension=dim, score=float(score)))
            eval_count += 1
    db.commit()
    print(f"✅ 教学评价: {eval_count}")

    # ── 7. Mode Templates ──
    for t in MODE_TEMPLATES:
        db.add(TeachingModeTemplate(**t))
    db.commit()
    print(f"✅ 教学模式模板: {len(MODE_TEMPLATES)}")

    # ── 8. Knowledge Graph (course 1 & 6) ──
    kg_nodes = KP_MAP[1]
    node_map = {}
    for i, name in enumerate(kg_nodes):
        obj = KnowledgeNode(name=name, course_id=1, parent_id=None, difficulty=KG_DIFFICULTY[i], order_index=i+1)
        db.add(obj)
        db.flush()
        node_map[i+1] = obj.id
    for src_i, tgt_i, rel in KG_EDGES:
        db.add(KnowledgeEdge(source_id=node_map[src_i], target_id=node_map[tgt_i], relation_type=rel))
    # Add simple graph for course 6 (AI)
    ai_nodes = KP_MAP[6]
    ai_map = {}
    for i, name in enumerate(ai_nodes):
        obj = KnowledgeNode(name=name, course_id=6, parent_id=None, difficulty=3.0+i*0.15, order_index=i+1)
        db.add(obj)
        db.flush()
        ai_map[i] = obj.id
    for i in range(len(ai_nodes)-1):
        db.add(KnowledgeEdge(source_id=ai_map[i], target_id=ai_map[i+1], relation_type="prerequisite"))
    db.commit()
    print(f"✅ 知识图谱: {len(kg_nodes)+len(ai_nodes)} 节点, {len(KG_EDGES)+len(ai_nodes)-1} 边")

    # ── 9. Audit Logs ──
    audit_actions = [
        ("admin", "data_import", "courses", 1, "导入课程数据：数据结构"),
        ("admin", "data_import", "classes", 1, "导入班级数据：12个班级"),
        ("admin", "data_import", "students", 1, f"导入学生数据：{total_students}人"),
        ("admin", "data_import", "grades", 1, f"导入成绩数据：{grade_count}条"),
        ("admin", "analysis_view", "class_profile", 1, "查看班级学情画像"),
        ("admin", "analysis_view", "diagnosis", 2, "生成诊断报告"),
        ("teacher_zhang", "mode_create", "mode", 1, "创建自定义教学模式"),
        ("teacher_zhang", "lesson_plan", "lesson_plan", 1, "生成智能备课教案"),
        ("teacher_li", "analysis_view", "comparison", 1, "执行A/B模式对比"),
        ("teacher_li", "reflection", "reflection", 2, "生成课后反思报告"),
    ]
    for user_id, action, entity_type, entity_id, details in audit_actions:
        db.add(AuditLog(user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id, details=details))
    db.commit()
    print(f"✅ 审计日志: {len(audit_actions)}")

    # ── 10. Notifications ──
    notifications = [
        ("teacher_zhang", "诊断报告已生成", "2024级软件工程1班的学情诊断报告已生成，请查看。", "diagnosis_ready", False),
        ("teacher_zhang", "A/B对比分析完成", "2024级软件工程1班 vs 2班的模式对比结果已出炉，Cohen's d = -0.36", "comparison_done", False),
        ("teacher_li", "模式迁移推荐", "检测到2024级计算机科学1班与软件工程2班学情相似度82%，推荐尝试实践驱动型模式", "migration_suggest", True),
        ("teacher_wang", "教学质量预警", "2024级网工2班近3次平均分持续下降，建议关注", "quality_alert", True),
        ("all", "系统更新", "学程智枢已升级至 v2.0，新增智能备课和课后反思功能", "system_update", False),
    ]
    for user_id, title, content, event_type, is_read in notifications:
        db.add(Notification(user_id=user_id, title=title, content=content, event_type=event_type, is_read=is_read))
    db.commit()
    print(f"✅ 消息通知: {len(notifications)}")

    # ── summary ──
    print("\n" + "="*50)
    print("🎉 全流程测试数据生成完毕！")
    print(f"   课程: {len(course_ids)} | 班级: {len(class_ids)} | 学生: {total_students}")
    print(f"   成绩: {grade_count} | 观察: {obs_count} | 评价: {eval_count}")
    print(f"   模式模板: {len(MODE_TEMPLATES)} | 审计: {len(audit_actions)} | 通知: {len(notifications)}")
    print(f"   知识图谱: 2门课程 {len(kg_nodes)+len(ai_nodes)} 节点")
    print("="*50)

    # Print demo path
    print("""
📋 推荐演示路径:
  1. Dashboard → 查看6门课程12个班级总览
  2. 数据导入 → 查看已导入的数据量
  3. 学情画像 → 对比优秀班(2班) vs 薄弱班(4班)
  4. A/B模式对比 → class_id=1 vs class_id=2 (Cohen's d)
  5. 模式指纹 → 查看互动讨论型/实践驱动型班级
  6. 教学模式库 → 浏览12种内置模板
  7. 知识图谱 → "数据结构"和"人工智能导论"两门
  8. 个体画像 → 查看学生个体的知识热力图
  9. 模式迁移 → 选薄弱班，查看相似优秀班的模式推荐
  10. 智能备课 → 选班级+课题生成教案
  11. 课后反思 → 生成达成度评估+改进建议
  12. 效果仪表盘 → 全景看板
  13. 通知中心 → 🔔查看5条示例通知
""")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Course).count() > 0:
            print("数据库已有数据，跳过播种。如需重新生成: rm xczs.db")
            db.close()
            sys.exit(0)
        seed(db)
    finally:
        db.close()
