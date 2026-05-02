"""
BabyGrow 安全审核层
自动检测医疗相关关键词，追加免责声明
"""

# 需要附加免责声明的关键词
MEDICAL_KEYWORDS = [
    "发烧", "发热", "高烧", "退烧", "体温",
    "咳嗽", "咳痰", "哮喘",
    "呕吐", "吐奶", "干呕",
    "腹泻", "拉肚子", "便血", "便秘",
    "皮疹", "湿疹", "过敏反应", "荨麻疹",
    "鼻涕", "鼻塞", "流鼻涕",
    "抽搐", "惊厥",
    "不吃奶", "拒奶", "厌奶",
    "黄疸",
]

# 严重症状 → 建议立即就医
SEVERE_KEYWORDS = [
    "抽搐", "惊厥", "呼吸困难", "嘴唇发紫",
    "便血", "高烧不退", "39度", "40度",
    "拒奶超过", "持续呕吐", "脱水",
]

# 用药相关关键词
MEDICATION_KEYWORDS = [
    "吃什么药", "用药", "药物", "剂量",
    "抗生素", "消炎药", "退烧药",
    "头孢", "阿莫西林", "布洛芬", "对乙酰氨基酚",
]


def review_response(content: str, question: str = "") -> dict:
    """
    审核 AI 回复，自动追加安全提示
    
    Returns:
        {
            "content": str,          # 可能追加了免责的回复
            "disclaimer": str|None,  # 追加的免责文本
            "severity": str,         # "safe" | "medical" | "medication" | "severe"
            "needs_disclaimer": bool
        }
    """
    combined = (content + " " + question).lower()
    
    # 严重症状检查（优先级最高）
    for keyword in SEVERE_KEYWORDS:
        if keyword in combined:
            disclaimer = (
                "\n\n⚠️ **重要提醒**：您描述的情况可能比较严重，"
                "建议尽快带宝宝就医，不要延误。以上信息仅供参考，不能替代专业医疗诊断。"
            )
            return {
                "content": content + disclaimer,
                "disclaimer": disclaimer,
                "severity": "severe",
                "needs_disclaimer": True
            }
    
    # 用药建议检查
    for keyword in MEDICATION_KEYWORDS:
        if keyword in combined:
            disclaimer = (
                "\n\n💊 **用药提醒**：以上用药建议仅供参考，"
                "具体用药请遵医嘱，切勿自行给宝宝用药。"
            )
            return {
                "content": content + disclaimer,
                "disclaimer": disclaimer,
                "severity": "medication",
                "needs_disclaimer": True
            }
    
    # 一般医疗症状检查
    for keyword in MEDICAL_KEYWORDS:
        if keyword in combined:
            disclaimer = (
                "\n\n🏥 **温馨提示**：以上建议仅供参考，"
                "如有疑问请咨询儿科医生。每个宝宝情况不同，专业医生的判断最重要。"
            )
            return {
                "content": content + disclaimer,
                "disclaimer": disclaimer,
                "severity": "medical",
                "needs_disclaimer": True
            }
    
    return {
        "content": content,
        "disclaimer": None,
        "severity": "safe",
        "needs_disclaimer": False
    }
