// ==================== KNOWLEDGE BASE ====================
window.KNOWLEDGE = (function() {

  // ===================== 食谱库 =====================
  var recipes = {
    '6-12': [
      {
        name: '南瓜小米糊', ageRange: '6月+', meals: [
          { time: '早餐', name: '南瓜小米糊', ingredients: [
            { name: '小米', amount: '20g' },
            { name: '南瓜', amount: '30g' },
            { name: '清水', amount: '200ml' }
          ], steps: [
            '小米提前浸泡10分钟，洗净备用',
            '南瓜去皮去籽，切成小块',
            '锅中加水，先放小米煮15分钟至软烂',
            '加入南瓜块再煮8分钟',
            '关火后用勺子捣成细腻的糊状',
            '放凉至40°C即可喂食'
          ], tips: '从稀糊开始，宝宝适应后逐渐加稠。南瓜富含胡萝卜素，对视力发育有益。', nutrition: '补铁/锌, 胡萝卜素' }
        ], tags: ['补铁', '辅食添加']
      },
      {
        name: '菠菜猪肝泥', ageRange: '6月+', meals: [
          { time: '午餐', name: '菠菜猪肝泥', ingredients: [
            { name: '猪肝', amount: '30g' },
            { name: '菠菜叶', amount: '15g' }
          ], steps: [
            '猪肝切薄片，用清水浸泡30分钟去血水',
            '换清水煮至完全熟透（约10分钟）',
            '菠菜洗净，焯水1分钟去除草酸',
            '猪肝和菠菜一起放入料理棒打成泥',
            '可加少量温水调成宝宝接受的稠度'
          ], tips: '猪肝是天然补铁食物，每周吃1-2次即可。菠菜焯水去草酸，不影响钙铁吸收。', nutrition: '补铁, 维生素A' }
        ], tags: ['补铁', '补维生素A']
      },
      {
        name: '苹果红薯泥', ageRange: '7月+', meals: [
          { time: '点心', name: '苹果红薯泥', ingredients: [
            { name: '苹果', amount: '30g' },
            { name: '红薯', amount: '30g' }
          ], steps: [
            '苹果洗净去皮切小块',
            '红薯去皮切小块',
            '一起蒸15分钟至软烂',
            '压成细腻的泥',
            '可加少量温水调稀'
          ], tips: '苹果带皮蒸营养更丰富，但一定要洗净。红薯富含膳食纤维，预防便秘。', nutrition: '膳食纤维, 维生素C' }
        ], tags: ['预防便秘', '维生素C']
      },
      {
        name: '胡萝卜牛肉泥', ageRange: '8月+', meals: [
          { time: '午餐', name: '胡萝卜牛肉泥', ingredients: [
            { name: '牛肉', amount: '40g' },
            { name: '胡萝卜', amount: '30g' }
          ], steps: [
            '牛肉切小块，浸泡去血水',
            '牛肉冷水下锅煮至熟透',
            '胡萝卜去皮切小块，蒸熟',
            '牛肉和胡萝卜一起打成泥',
            '可加少量牛肉汤调稀'
          ], tips: '牛肉选择里脊部位，脂肪少。8月龄后可从稀糊过渡到有颗粒的蓉状。', nutrition: '优质蛋白, 补铁, 胡萝卜素' }
        ], tags: ['补铁', '优质蛋白']
      },
      {
        name: '西兰花鳕鱼泥', ageRange: '9月+', meals: [
          { time: '晚餐', name: '西兰花鳕鱼泥', ingredients: [
            { name: '鳕鱼', amount: '40g' },
            { name: '西兰花', amount: '30g' }
          ], steps: [
            '鳕鱼去皮去骨，切小块',
            '柠檬片盖在鱼上蒸8分钟去腥',
            '西兰花焯水2分钟切碎',
            '鱼肉和西兰花一起打成泥',
            '加少量温水调至宝宝适合的稠度'
          ], tips: '鳕鱼刺少肉嫩，是优质的DHA来源。西兰花要切得细碎，避免噎住。', nutrition: 'DHA, 膳食纤维' }
        ], tags: ['补DHA', '益智']
      },
      {
        name: '山药苹果糊', ageRange: '6月+', meals: [
          { time: '早餐', name: '山药苹果糊', ingredients: [
            { name: '山药', amount: '30g' },
            { name: '苹果', amount: '25g' }
          ], steps: [
            '山药去皮切小块（处理时戴手套防粘液）',
            '苹果去皮切小块',
            '一起蒸12分钟至软烂',
            '压成糊状，可加少量温水'
          ], tips: '山药健脾养胃，对消化不良的宝宝有好处。黏液是营养成分，不要洗掉。', nutrition: '健脾, 膳食纤维' }
        ], tags: ['健脾', '易消化']
      },
      {
        name: '蛋黄溶豆', ageRange: '8月+', meals: [
          { time: '点心', name: '蛋黄溶豆', ingredients: [
            { name: '鸡蛋黄', amount: '2个' },
            { name: '婴儿奶粉', amount: '10g' },
            { name: '柠檬汁', amount: '几滴' }
          ], steps: [
            '鸡蛋煮熟，取蛋黄',
            '蛋黄加柠檬汁用打蛋器打发至颜色变浅',
            '筛入奶粉，轻轻翻拌',
            '装入裱花袋，挤到烤盘上（小米粒大小）',
            '烤箱90°C烤40分钟至酥脆'
          ], tips: '入口即溶，锻炼宝宝手眼协调。适合抓握练习。无蛋清，不易过敏。', nutrition: '卵磷脂, 维生素A' }
        ], tags: ['手指食物', '锻炼抓握']
      }
    ],
    '12-18': [
      {
        name: '西红柿鸡蛋面', ageRange: '12月+', meals: [
          { time: '午餐', name: '西红柿鸡蛋面', ingredients: [
            { name: '婴幼儿面条', amount: '30g' },
            { name: '西红柿', amount: '半个' },
            { name: '鸡蛋', amount: '1个' },
            { name: '清水', amount: '300ml' }
          ], steps: [
            '西红柿划十字，热水烫去皮，切碎',
            '鸡蛋打散备用',
            '锅中加水煮开，下面条煮5分钟',
            '另起锅炒西红柿至出汁',
            '加入面条和适量汤水煮开',
            '淋入蛋液，蛋花形成后关火'
          ], tips: '面条要煮软烂一些。鸡蛋可以换成肉末，做成西红柿肉末面。', nutrition: '优质蛋白, 维生素C' }
        ], tags: ['优质蛋白', '快手']
      },
      {
        name: '番茄牛肉丸', ageRange: '13月+', meals: [
          { time: '午餐', name: '番茄牛肉丸', ingredients: [
            { name: '牛肉糜', amount: '50g' },
            { name: '番茄', amount: '1个' },
            { name: '淀粉', amount: '5g' },
            { name: '葱姜水', amount: '少许' }
          ], steps: [
            '牛肉糜加淀粉和葱姜水搅拌上劲',
            '搓成小丸子（每颗约10g）',
            '番茄去皮切小块',
            '牛肉丸冷水下锅煮至浮起',
            '另起锅炒番茄出汁，加水煮开',
            '放入牛肉丸煮3分钟即可'
          ], tips: '牛肉糜加少量肥肉口感更嫩。1岁后可以加少量盐调味。', nutrition: '补铁, 优质蛋白' }
        ], tags: ['补铁', '手指食物']
      },
      {
        name: '三鲜蛋炒饭', ageRange: '14月+', meals: [
          { time: '午餐', name: '三鲜蛋炒饭', ingredients: [
            { name: '软米饭', amount: '1小碗' },
            { name: '鸡蛋', amount: '1个' },
            { name: '胡萝卜', amount: '10g' },
            { name: '西兰花', amount: '10g' },
            { name: '油', amount: '3g' }
          ], steps: [
            '胡萝卜、西兰花焯水切碎',
            '鸡蛋打散',
            '热锅凉油，先炒鸡蛋至嫩滑盛出',
            '再放少量油，炒蔬菜丁',
            '加入米饭翻炒松散',
            '加入鸡蛋碎翻炒均匀'
          ], tips: '1岁半后宝宝可以吃炒饭了，但还是要做得软一些。少放油，蔬菜切碎一些。', nutrition: '碳水, 蛋白质, 膳食纤维' }
        ], tags: ['锻炼咀嚼', '快手']
      },
      {
        name: '紫菜虾皮汤', ageRange: '12月+', meals: [
          { time: '早餐', name: '紫菜虾皮汤', ingredients: [
            { name: '紫菜', amount: '3g' },
            { name: '虾皮', amount: '3g' },
            { name: '鸡蛋', amount: '1个' },
            { name: '清水', amount: '200ml' }
          ], steps: [
            '紫菜撕碎，虾皮洗净',
            '清水煮开，放入紫菜和虾皮',
            '再次煮开后淋入蛋液',
            '关火，加少量香油调味'
          ], tips: '紫菜虾皮都是天然补钙食材。虾皮要选无盐的。1岁后可以少量加盐。', nutrition: '补钙, 碘' }
        ], tags: ['补钙', '快手汤']
      },
      {
        name: '南瓜发糕', ageRange: '12月+', meals: [
          { time: '点心', name: '南瓜发糕', ingredients: [
            { name: '南瓜', amount: '50g' },
            { name: '面粉', amount: '40g' },
            { name: '牛奶或配方奶', amount: '30ml' },
            { name: '酵母', amount: '1g' },
            { name: '鸡蛋', amount: '半个' }
          ], steps: [
            '南瓜蒸熟压成泥，晾凉',
            '酵母加少量温水活化',
            '南瓜泥+面粉+酵母+蛋液+奶混合搅匀',
            '模具刷油，倒入面糊',
            '发酵30分钟（夏天），或蒸锅水热后发酵',
            '水开后蒸15分钟，焖2分钟'
          ], tips: '发糕松软好消化，比蛋糕更适合小宝宝。可以冷冻保存，吃时蒸热。', nutrition: '碳水, 维生素A' }
        ], tags: ['锻炼咀嚼', '手指食物']
      },
      {
        name: '蔬菜肉末馄饨', ageRange: '14月+', meals: [
          { time: '午餐', name: '蔬菜肉末馄饨', ingredients: [
            { name: '馄饨皮', amount: '适量' },
            { name: '猪肉糜', amount: '40g' },
            { name: '青菜', amount: '20g' },
            { name: '葱姜', amount: '少许' },
            { name: '馄饨汤底', amount: '紫菜虾皮汤底' }
          ], steps: [
            '青菜焯水切碎挤干',
            '肉糜+青菜+葱姜搅拌上劲',
            '馄饨皮包入适量肉馅，对折捏紧',
            '水开下馄饨，浮起后再煮2分钟',
            '配紫菜虾皮汤一起吃'
          ], tips: '馄饨皮可以切小一点给宝宝。冷冻保存，一次多做些备着。', nutrition: '优质蛋白, 蔬菜纤维' }
        ], tags: ['锻炼咀嚼', '可冷冻']
      }
    ],
    '18-24': [
      {
        name: '彩虹蔬菜炒饭', ageRange: '18月+', meals: [
          { time: '午餐', name: '彩虹蔬菜炒饭', ingredients: [
            { name: '软米饭', amount: '1小碗' },
            { name: '鸡蛋', amount: '1个' },
            { name: '胡萝卜', amount: '15g' },
            { name: '豌豆', amount: '10g' },
            { name: '玉米粒', amount: '10g' },
            { name: '油', amount: '5g' }
          ], steps: [
            '胡萝卜切小丁，豌豆玉米焯水',
            '鸡蛋打散备用',
            '热锅放油，先炒鸡蛋至嫩滑盛出',
            '再炒胡萝卜丁2分钟',
            '加入米饭翻炒松散',
            '加入鸡蛋和蔬菜丁炒匀，可加少量盐'
          ], tips: '颜色丰富引起宝宝兴趣。蔬菜切细小，避免只吃饭不吃菜。', nutrition: '碳水, 蛋白质, 维生素' }
        ], tags: ['吸引宝宝', '营养均衡']
      },
      {
        name: '红烧鱼块（去骨）', ageRange: '20月+', meals: [
          { time: '晚餐', name: '红烧鱼块', ingredients: [
            { name: '无骨鱼块', amount: '60g' },
            { name: '西红柿', amount: '半个' },
            { name: '酱油', amount: '几滴' },
            { name: '葱姜', amount: '适量' },
            { name: '油', amount: '5g' }
          ], steps: [
            '鱼块用厨房纸吸干水分',
            '热锅少油，葱姜爆香',
            '放鱼块煎至两面微黄',
            '加入西红柿块和少量水',
            '中小火焖煮10分钟至鱼熟透',
            '收汁，可加少量儿童酱油调味'
          ], tips: '2岁后可以尝试红烧。选刺少肉嫩的鱼，如鳕鱼、鲈鱼。一定要仔细检查无刺。', nutrition: '优质蛋白, DHA' }
        ], tags: ['补DHA', '2岁+']
      },
      {
        name: '虾仁豆腐煲', ageRange: '18月+', meals: [
          { time: '午餐', name: '虾仁豆腐煲', ingredients: [
            { name: '虾仁', amount: '30g' },
            { name: '嫩豆腐', amount: '30g' },
            { name: '蘑菇', amount: '10g' },
            { name: '葱姜水', amount: '少许' }
          ], steps: [
            '虾仁去虾线，用葱姜水去腥',
            '豆腐切小方块',
            '蘑菇切片焯水',
            '锅中加水，放豆腐和蘑菇煮开',
            '放入虾仁煮至变色',
            '加少量水淀粉勾薄芡'
          ], tips: '虾仁富含钙，豆腐富含植物蛋白。两者搭配营养互补。', nutrition: '补钙, 优质蛋白' }
        ], tags: ['补钙', '鲜香']
      },
      {
        name: '西红柿牛腩面', ageRange: '20月+', meals: [
          { time: '午餐', name: '西红柿牛腩面', ingredients: [
            { name: '婴幼儿面条', amount: '40g' },
            { name: '牛腩', amount: '40g' },
            { name: '西红柿', amount: '1个' },
            { name: '洋葱', amount: '少量' }
          ], steps: [
            '牛腩切小块，焯水去血沫',
            '西红柿去皮切块，洋葱切丝',
            '牛腩先炖煮40分钟至软烂',
            '另起锅炒西红柿洋葱出汁',
            '加入牛腩和汤水煮开',
            '下入面条煮至软烂'
          ], tips: '牛腩提前炖好冷冻起来，下次拿出来直接用很方便。2岁后可以这样吃。', nutrition: '补铁, 优质蛋白' }
        ], tags: ['补铁', '周末备餐']
      },
      {
        name: '杂蔬鸡肉串', ageRange: '18月+', meals: [
          { time: '点心', name: '杂蔬鸡肉串', ingredients: [
            { name: '鸡胸肉', amount: '40g' },
            { name: '彩椒', amount: '各色10g' },
            { name: '洋葱', amount: '少量' },
            { name: '淀粉', amount: '少量' }
          ], steps: [
            '鸡胸肉切小块，加少量淀粉抓嫩',
            '彩椒、洋葱切跟鸡肉差不多大小的块',
            '用竹签交替串起来（竹签提前泡水）',
            '平底锅少油，小火煎至鸡肉熟透',
            '中途翻面，约8-10分钟'
          ], tips: '切成手指大小的块，方便抓着吃。彩椒颜色鲜艳增加食欲。', nutrition: '蛋白质, 维生素C' }
        ], tags: ['手指食物', '锻炼自主进食']
      }
    ],
    '24-36': [
      {
        name: '红烧鱼块（去骨）', ageRange: '24月+', meals: [
          { time: '午餐', name: '红烧鱼块', ingredients: [
            { name: '无骨鱼块', amount: '80g' },
            { name: '西红柿', amount: '1个' },
            { name: '儿童酱油', amount: '少量' },
            { name: '葱姜', amount: '适量' }
          ], steps: [
            '鱼块吸干水分，热锅少油煎至两面金黄',
            '葱姜爆香，放西红柿块炒出汁',
            '加少量水和酱油，放入鱼块',
            '中小火焖煮15分钟',
            '大火收汁，注意翻面'
          ], tips: '2岁后可以正常吃红烧口味了。选择刺少的鱼，彻底检查无刺。', nutrition: '优质蛋白, DHA' }
        ], tags: ['家常菜', '补DHA']
      },
      {
        name: '虾仁豆腐煲', ageRange: '24月+', meals: [
          { time: '午餐', name: '虾仁豆腐煲', ingredients: [
            { name: '虾仁', amount: '40g' },
            { name: '嫩豆腐', amount: '50g' },
            { name: '蘑菇', amount: '15g' },
            { name: '水淀粉', amount: '适量' }
          ], steps: [
            '虾仁去虾线，豆腐切块',
            '蘑菇切片',
            '锅中加水放豆腐和蘑菇煮开',
            '放入虾仁煮至变色',
            '加水淀粉勾芡',
            '可加少量盐和香油'
          ], tips: '可以多放虾和豆腐，增加蛋白质。汤汁拌饭也很开胃。', nutrition: '补钙, 优质蛋白' }
        ], tags: ['补钙', '快手']
      },
      {
        name: '蒜蓉西兰花', ageRange: '24月+', meals: [
          { time: '午餐', name: '蒜蓉西兰花', ingredients: [
            { name: '西兰花', amount: '100g' },
            { name: '大蒜', amount: '1瓣' },
            { name: '油', amount: '5g' }
          ], steps: [
            '西兰花切小朵，焯水2分钟捞出',
            '大蒜切末',
            '热锅少油，蒜末爆香',
            '放入西兰花快速翻炒',
            '加少量盐调味即可'
          ], tips: '西兰花焯水后再炒，颜色更翠绿，也更容易熟。大蒜有杀菌作用。', nutrition: '维生素C, 膳食纤维' }
        ], tags: ['蔬菜', '家常菜']
      },
      {
        name: '肉末蒸蛋', ageRange: '24月+', meals: [
          { time: '午餐', name: '肉末蒸蛋', ingredients: [
            { name: '鸡蛋', amount: '2个' },
            { name: '猪肉糜', amount: '30g' },
            { name: '葱姜水', amount: '少许' }
          ], steps: [
            '鸡蛋打散，加1.5倍温水搅匀',
            '过筛到蒸碗中，盖保鲜膜',
            '蒸锅水开，中火蒸8分钟',
            '猪肉糜加葱姜水炒散至熟',
            '蒸蛋凝固后铺上肉末',
            '再蒸2分钟即可'
          ], tips: '蛋液过筛口感更细腻。加肉末时等蛋液凝固再放，否则会沉底。', nutrition: '优质蛋白, 铁' }
        ], tags: ['快手', '补铁']
      },
      {
        name: '冬瓜排骨汤', ageRange: '24月+', meals: [
          { time: '午餐', name: '冬瓜排骨汤', ingredients: [
            { name: '排骨', amount: '50g' },
            { name: '冬瓜', amount: '80g' },
            { name: '姜片', amount: '2片' }
          ], steps: [
            '排骨焯水去血沫',
            '砂锅加水，放入排骨和姜片炖40分钟',
            '冬瓜去皮切块',
            '加入冬瓜再煮15分钟至透明',
            '加少量盐调味'
          ], tips: '排骨汤是经典的补钙汤品。冬瓜利尿，适合夏天喝。2岁后可以正常加盐。', nutrition: '补钙, 优质蛋白' }
        ], tags: ['补钙', '经典汤品']
      },
      {
        name: '番茄肉酱意面', ageRange: '24月+', meals: [
          { time: '午餐', name: '番茄肉酱意面', ingredients: [
            { name: '意面', amount: '40g' },
            { name: '猪肉糜', amount: '40g' },
            { name: '番茄', amount: '1个' },
            { name: '洋葱', amount: '少量' }
          ], steps: [
            '番茄去皮切碎，洋葱切末',
            '意面煮软煮透，约10分钟',
            '热锅炒肉糜至变色盛出',
            '再炒洋葱软，加番茄炒出汁',
            '加少量水焖煮成酱',
            '加入肉糜和意面翻炒均匀'
          ], tips: '番茄肉酱可以一次多做冷冻保存，下次拿出来直接拌面。', nutrition: '碳水, 蛋白质' }
        ], tags: ['宝宝西餐', '趣味饮食']
      }
    ]
  };

  // ===================== 游戏库 =====================
  var games = [
    // 6-12月龄
    { name: '积木敲敲乐', ageRange: [6,12], type: '精细动作', duration: '10分钟', materials: '软积木',
      steps: ['把积木放在桌上或地垫上', '家长示范用手把积木敲倒，发出"哗啦"声', '鼓励宝宝伸手去敲积木', '每次敲倒后给予热烈回应："哇！你敲倒了！"', '引导宝宝把积木重新堆起来再敲'],
      benefits: '手眼协调, 因果关系认知, 触觉探索', tips: '选择软积木，防止磕碰。积木大小适合抓握。' },
    { name: '镜子里的宝宝', ageRange: [6,12], type: '认知', duration: '5分钟', materials: '镜子',
      steps: ['抱着宝宝站在镜子前', '指着镜中的宝宝说"这是谁呀？这是宝宝！"', '指着镜中的妈妈说"这是妈妈！"', '引导宝宝伸手去摸镜中的"宝宝"', '变换角度，让宝宝看到不同反射'],
      benefits: '自我认知, 情感连接', tips: '宝宝会突然对镜子里的自己产生好奇，这是自我意识萌芽的标志。' },
    { name: '藏猫猫', ageRange: [6,12], type: '认知', duration: '5分钟', materials: '无',
      steps: ['家长用手遮住自己的脸说"妈妈在哪里？"', '突然打开手说"喵！妈妈在这里！"', '观察宝宝的表情变化', '可以让宝宝尝试用手遮住脸，家长来找'],
      benefits: '物体恒存概念, 分离焦虑缓解', tips: '藏猫猫能帮助宝宝理解"东西看不见不等于不存在"，这是重要的认知里程碑。' },
    { name: '抽纸巾游戏', ageRange: [8,12], type: '精细动作', duration: '10分钟', materials: '纸巾盒',
      steps: ['把纸巾盒放在宝宝够得到的地方', '家长示范抽出纸巾，一张一张地抽', '让宝宝尝试自己抽出纸巾', '引导宝宝把纸巾揉成团', '把纸巾团扔进垃圾桶'],
      benefits: '精细动作, 空间认知, 动手能力', tips: '宝宝会非常享受抽纸巾的过程，这是练习手指的好机会。' },
    { name: '爬行隧道', ageRange: [8,12], type: '大运动', duration: '15分钟', materials: '枕头/大箱子/爬行隧道玩具',
      steps: ['用枕头或箱子设置一个简单的"隧道"', '在隧道另一头叫宝宝的名字', '用玩具或声音吸引宝宝注意力', '鼓励宝宝爬过隧道', '完成后给予大大的拥抱和表扬'],
      benefits: '爬行能力, 空间感知, 勇气培养', tips: '确保隧道安全，入口出口都有软垫。' },
    { name: '牙胶啃咬', ageRange: [6,12], type: '口腔', duration: '随时', materials: '各种形状牙胶',
      steps: ['提供不同形状和材质的牙胶', '示范放进嘴里啃咬', '观察宝宝喜欢哪种形状', '定期清洗消毒牙胶'],
      benefits: '口腔探索, 出牙期缓解', tips: '牙胶放冰箱冷藏一下，能更好地缓解出牙不适。不要冷冻。' },
    { name: '撕纸游戏', ageRange: [8,12], type: '精细动作', duration: '10分钟', materials: '广告纸/皱纹纸',
      steps: ['给宝宝干净的纸', '示范撕纸的动作', '让宝宝尝试撕纸', '把撕下的纸条收集起来', '可以说"我们把纸撕成了小碎片！"'],
      benefits: '手指力量, 触觉探索', tips: '皱纹纸比普通纸更容易撕开，更适合小宝宝。' },
    // 12-18月龄
    { name: '蜡笔涂鸦', ageRange: [12,18], type: '精细动作', duration: '15分钟', materials: '可水洗蜡笔+大纸',
      steps: ['把蜡笔和纸放在地垫上', '家长示范拿起蜡笔在纸上画圈', '鼓励宝宝拿起蜡笔', '让宝宝自由地在纸上涂画', '画完后一起欣赏作品："这是一辆车！"'],
      benefits: '精细动作, 创造力, 颜色认知', tips: '可水洗蜡笔非常好清理。选择大纸，减少画到地上和墙上。' },
    { name: '堆堆乐', ageRange: [12,18], type: '精细动作', duration: '15分钟', materials: '塑料杯/软积木',
      steps: ['示范把杯子一个一个叠起来', '让宝宝尝试叠高', '叠好后一起数"1、2、3！"', '鼓励宝宝推倒（这部分他们最擅长！）', '推倒后再重新叠'],
      benefits: '空间感, 平衡感, 数数启蒙', tips: '塑料杯是很好的低成本玩具，可以叠出各种形状。' },
    { name: '球类滚动', ageRange: [12,18], type: '大运动', duration: '15分钟', materials: '软球',
      steps: ['和宝宝面对面坐好，距离1-2米', '家长示范把球滚向宝宝', '请宝宝把球滚回来', '球停住后，夸张地接住说"我接到了！"', '可以慢慢加大距离'],
      benefits: '手眼协调, 社交互动, 肢体协调', tips: '选择软质轻量的小球，避免砸伤。' },
    { name: '翻翻卡', ageRange: [12,18], type: '语言/认知', duration: '10分钟', materials: '动物卡片',
      steps: ['展示一张动物卡片，如小猫', '示范动物的叫声"喵喵~"', '做出动物的动作，如小猫挠东西', '请宝宝来模仿', '每张卡片停留10-20秒'],
      benefits: '语言发育, 动物认知, 模仿能力', tips: '选择真实的动物图片，不是卡通形象。' },
    { name: '套圈圈', ageRange: [15,18], type: '精细动作', duration: '15分钟', materials: '套圈玩具',
      steps: ['示范如何把圈圈套进去', '让宝宝尝试套圈', '成功后给予大大的表扬', '可以按颜色分类套', '逐渐加大难度，套到更远的柱子上'],
      benefits: '手眼协调, 专注力, 颜色分类', tips: '选择大孔的套圈玩具，更适合低龄宝宝。' },
    { name: '锅碗瓢盆敲敲乐', ageRange: [12,18], type: '音乐', duration: '15分钟', materials: '不锈钢碗/木勺/塑料盆',
      steps: ['把锅碗放在地上', '家长示范用木勺敲打，发出声音', '引导宝宝拿起勺子敲', '一起敲出节奏："咚-咚咚-咚！"', '可以让不同大小的碗发出不同音高'],
      benefits: '音乐启蒙, 节奏感, 声音认知', tips: '这是宝宝最爱的敲打游戏之一，完全不需要买玩具。' },
    { name: '贴贴纸', ageRange: [15,18], type: '精细动作', duration: '15分钟', materials: '贴纸书或大贴纸',
      steps: ['选择适合的贴纸书', '示范如何撕开贴纸', '引导宝宝把贴纸贴在正确位置', '一起欣赏完成的画面', '可以拍下作品留念'],
      benefits: '精细动作, 专注力, 认知', tips: '选择大张、容易撕取的贴纸。太小的贴纸对1岁宝宝太难。' },
    // 18-24月龄
    { name: '过家家', ageRange: [18,24], type: '想象', duration: '20分钟', materials: '玩具厨具/娃娃/道具',
      steps: ['设置场景，如厨房、诊所、超市', '家长先示范玩法："我来当妈妈做饭"→假装切菜', '引导宝宝加入："宝宝来尝尝妈妈做的菜"→假装喂娃娃', '让宝宝主导，家长跟随扮演', '结束后一起"收拾厨房"'],
      benefits: '想象力, 社交能力, 生活技能认知', tips: '不需要买专门的过家家玩具，日常生活中的一切都可以扮演。' },
    { name: '沙子/大米感官盒', ageRange: [18,24], type: '感官', duration: '20分钟', materials: '大米/沙子+小玩具+盒子',
      steps: ['在大盒子里放满大米或沙子', '藏入一些小玩具', '家长示范用手在米里"寻宝"', '请宝宝也来找宝贝', '找到后引导宝宝描述："你找到了什么？"'],
      benefits: '触觉探索, 专注力, 描述能力', tips: '大米比沙子干净安全，可以在室内玩。加点水会有不同质感。' },
    { name: '串珠子（大孔）', ageRange: [18,24], type: '精细动作', duration: '15分钟', materials: '粗绳+大木珠/通心粉',
      steps: ['示范把绳子穿过珠子的孔', '让宝宝尝试自己穿', '穿好后可以戴在脖子上（需监督）', '可以做一条长长的"项链"', '引导边穿边数"1、2、3..."'],
      benefits: '专注力, 手眼协调, 数数启蒙', tips: '必须选择大孔的珠子，或者用通心粉（空心面）代替木珠，更安全。' },
    { name: '模仿游戏', ageRange: [18,24], type: '想象', duration: '15分钟', materials: '无',
      steps: ['和家长面对面坐好', '家长说"我们来做刷牙操！"→示范刷牙动作', '宝宝模仿刷牙动作', '换其他动作：洗脸、梳头、擦香香', '可以说"你刷牙刷得真干净！"'],
      benefits: '生活技能, 模仿能力, 身体协调', tips: '把日常动作变成游戏，宝宝会更有动力学习生活技能。' },
    { name: '涂色书', ageRange: [18,24], type: '精细动作', duration: '15分钟', materials: '大格涂色书+蜡笔',
      steps: ['选择图案简单、线条粗的涂色书', '示范在格子里涂色，不涂出边', '让宝宝自由涂色', '完成后一起给作品起名字', '可以贴在墙上展示'],
      benefits: '精细动作, 颜色认知, 专注力', tips: '不要在意涂得"对不对"，过程比结果重要。' },
    { name: '积木火车', ageRange: [18,24], type: '想象', duration: '15分钟', materials: '积木',
      steps: ['把积木排成长长一列', '家长说"呜——！火车要开啦！"', '和宝宝一起推着积木"火车"在房间里开', '经过"山洞"（椅子下面）时说"进山洞啦"', '模仿火车的声音："呜~呜~呜~"'],
      benefits: '想象力, 大运动, 语言发展', tips: '这个游戏可以让宝宝安静下来，适合在吵闹后玩。' },
    // 2-3岁
    { name: '角色扮演游戏', ageRange: [24,36], type: '想象', duration: '30分钟', materials: '角色扮演服装/道具',
      steps: ['设置场景：医生诊所/超市/厨房/消防员', '分配角色，家长先示范', '宝宝扮演主要角色，家长扮演配合者', '让宝宝主导剧情发展', '结束后一起收拾道具'],
      benefits: '社会认知, 想象力, 表达能力', tips: '医生游戏可以减轻宝宝对看医生的恐惧。' },
    { name: '料理小帮手', ageRange: [24,36], type: '生活技能', duration: '30分钟', materials: '安全蔬菜/工具',
      steps: ['给宝宝分配简单任务：洗菜/搅拌/摆盘', '示范如何做（如：用塑料刀切软香蕉）', '让宝宝完成自己的"工作"', '完成后说"谢谢你帮忙！"', '一起享用劳动成果'],
      benefits: '生活技能, 成就感, 参与感', tips: '一定要用安全的儿童刀具，即使切不断也能锻炼。不要催促，让宝宝慢慢来。' },
    { name: '户外探索', ageRange: [24,36], type: '自然认知', duration: '30分钟', materials: '无',
      steps: ['去公园或小区绿地', '一起找不同颜色的树叶', '观察蚂蚁搬家（蹲下来看）', '听鸟叫声，问"这是什么鸟？"', '捡一些安全的"宝贝"带回家'],
      benefits: '自然认知, 观察力, 好奇心', tips: '不要催促，跟着宝宝的节奏。宝宝蹲下来看蚂蚁时，耐心等他。' },
    { name: '手指画', ageRange: [24,36], type: '艺术', duration: '20分钟', materials: '可水洗颜料+大白纸',
      steps: ['铺好报纸，穿上旧衣服', '在托盘里放少量颜料', '示范用手指在颜料里蘸一蘸', '在纸上印手指印或涂抹', '完成后一起给画起名字'],
      benefits: '创造力, 感官探索, 艺术表达', tips: '选择可水洗颜料，脏了也不怕。颜料可以混色，让宝宝观察变化。' },
    { name: '简单的科学实验', ageRange: [24,36], type: '科学思维', duration: '15分钟', materials: '水杯+不同物体（会浮/会沉的）',
      steps: ['准备一盆水和各种小物件', '家长先猜"这个会浮起来还是沉下去？"', '把物件放进水里观察', '一起分类：浮起来的/沉下去的', '问"为什么木头会浮，铁就沉呢？"'],
      benefits: '科学思维, 观察力, 好奇心', tips: '适合在洗澡时玩，更方便。' },
    { name: '假装打电话', ageRange: [24,36], type: '语言', duration: '10分钟', materials: '玩具电话或纸筒',
      steps: ['用玩具电话或卷纸筒当电话', '家长假装打电话："喂，是奶奶吗？"', '让宝宝来接："喂！奶奶好！"', '进行简单的对话："你今天做什么了？"', '让宝宝也来"打电话"给爷爷奶奶'],
      benefits: '语言发展, 社交技能, 想象力', tips: '可以趁这个机会让宝宝和爷爷奶奶通话，一举两得。' }
  ];

  // ===================== 故事库 =====================
  var stories = [
    // 6-12月龄（布书/翻翻书）
    { name: '小熊好忙系列', author: 'Rod Machin', ageRange: [6,12], duration: '2-3分钟/本', type: '布书',
      description: '中英双语的互动机关书，每页有小机关可以推、拉、转。内容是宝宝日常生活场景（洗澡、睡觉、去公园等）。',
      howToTell: '放慢语速，边讲故事边操作机关，让宝宝参与。读到"shake"就摇晃书本。',
      themes: ['日常生活', '中英双语', '互动'],
      tips: '适合6月龄开始，当作亲子互动的工具，而不是真的讲故事。' },
    { name: '猜猜我是谁系列', author: 'Nina Lumpur', ageRange: [6,12], duration: '3分钟', type: '洞洞纸板书',
      description: '每页有个洞洞，翻到下一页洞洞变成动物的一部分，最后揭示完整的动物。共7本。',
      howToTell: '先让宝宝从洞洞猜"这是什么？"→ 翻页揭示答案"是小猫！喵呜~"',
      themes: ['动物认知', '好奇心', '猜测游戏'],
      tips: '最后揭秘时配合夸张的表情，增加惊喜感。' },
    { name: '好饿的毛毛虫', author: 'Eric Carle', ageRange: [6,12], duration: '3分钟', type: '纸板书',
      description: '一条毛毛虫从蛋里出来，每天吃不同的食物，从星期一吃到星期六，最后变成美丽的蝴蝶。',
      howToTell: '数数手指（一根两根三根），模仿吃东西的声音（咕叽咕叽），最后一起"哇！"变蝴蝶。',
      themes: ['数字', '食物认知', '星期', '生命周期'],
      tips: '洞洞设计让宝宝可以戳着玩。颜色鲜艳，吸引注意力。' },
    { name: '我爸爸', author: 'Anthony Browne', ageRange: [6,12], duration: '3分钟', type: '纸板书',
      description: '我爸爸什么都不怕，连大野狼都不怕。他像猩猩一样强壮，像河马一样快乐。',
      howToTell: '用宝宝熟悉的家人做比喻："像爸爸一样高，像妈妈一样温柔"。最后抱住宝宝说"你也像爸爸一样勇敢！"',
      themes: ['亲情', '爸爸形象', '安全感'],
      tips: '每页都有藏在画面里的小秘密，如爸爸鼻子上有个小球。适合多次阅读后发现。' },
    { name: '我妈妈', author: 'Anthony Browne', ageRange: [6,12], duration: '3分钟', type: '纸板书',
      description: '我妈妈是个手艺特好的大厨师，是个杂技演员，是个有魔法的园丁。她的歌像天使一样好听。',
      howToTell: '唱一唱书里妈妈唱的歌，表演书里妈妈做的动作。结尾拥抱宝宝。',
      themes: ['亲情', '妈妈形象', '职业认知'],
      tips: '和《我爸爸》一起读，建立完整的家庭形象。' },
    { name: '抱抱', author: 'Jez Alborough', ageRange: [6,12], duration: '2分钟', type: '纸板书',
      description: '小猩猩找不到妈妈，其他动物给它温暖的抱抱。最后小猩猩的妈妈出现了，给它一个大大的拥抱。',
      howToTell: '每次看到"抱抱"这个词，就真的抱一下宝宝。看到其他动物给宝宝抱抱，也抱一下。',
      themes: ['亲情', '拥抱', '分离焦虑'],
      tips: '文字很少，主要靠画面和"抱抱"来传达情感。很适合睡前读。' },
    { name: '小金鱼逃走了', author: '五味太郎', ageRange: [6,12], duration: '3分钟', type: '纸板书',
      description: '一条红色的小金鱼从鱼缸里逃走了，它躲在各种地方——鱼缸里（其实不是）、金鱼缸外面、花盆里、糖果罐里……',
      howToTell: '每翻一页先问"金鱼在哪里？"，然后指出逃跑的金鱼。最后一页金鱼在镜子里，意味着它找到了同伴。',
      themes: ['观察力', '金鱼', '找东西'],
      tips: '锻炼宝宝的专注力和观察力，让宝宝来找金鱼。' },
    { name: '点点点', author: 'Hervé Tullet', ageRange: [9,12], duration: '5分钟', type: '互动书',
      description: '黄色的点、按一下变多、摇一摇颜色混在一起、对着书吹气点点乱飞……',
      howToTell: '完全按照书上写的做！按一下、摇一摇、吹口气、两只手合起来拍一下。宝宝会疯狂爱上这本书。',
      themes: ['颜色', '数量', '互动'],
      tips: '读这本书要动起来，不是坐着看。非常消耗精力，适合睡前读。' },
    // 12-18月龄
    { name: '晚安大猩猩', author: 'Peggy Rathmann', ageRange: [12,18], duration: '5分钟', type: '睡前故事',
      description: '动物园管理员晚上去跟动物们说晚安，但大猩猩偷走了钥匙，把所有动物都放出来，大家一起跟在管理员身后回家了……',
      howToTell: '每翻一页问"这是谁？"→认识各种动物。最后动物们偷偷回家的场景很温馨。睡前仪式感。',
      themes: ['睡前', '动物', '幽默'],
      tips: '文字少，全靠画面讲故事。适合已经开始认识动物的宝宝。' },
    { name: '菲菲生气了', author: 'Molly Bang', ageRange: [12,18], duration: '3分钟', type: '情绪绘本',
      description: '菲菲的姐姐抢走了她的玩具，菲菲气疯了——她的火气大到整个房间都变小了。她跑出去哭了一场，看了看大自然，慢慢平静下来。',
      howToTell: '菲菲生气时用大一点的声音和夸张的表情，让宝宝感受到情绪的强度。平静后恢复轻声。',
      themes: ['情绪管理', '生气', '平静'],
      tips: '帮助宝宝认识"生气"这种情绪，知道生气是正常的，但会过去。' },
    { name: '爷爷一定有办法', author: 'Judith Craighead', ageRange: [12,18], duration: '5分钟', type: '亲情绘本',
      description: '爷爷给约瑟做了一条毯子，后来小了破了，爷爷把它变成了外套、外套变成背心……最后变成了一颗纽扣。',
      howToTell: '边讲故事边指着画面里的小老鼠一家（它们也在用布料做东西），增加探索乐趣。',
      themes: ['亲情', '节俭', '创造力', '爷爷'],
      tips: '培养节俭意识，告诉宝宝旧东西也可以变出新花样。' },
    { name: '母鸡萝丝去散步', author: 'Peggy Rathmann', ageRange: [12,18], duration: '3分钟', type: '幽默绘本',
      description: '母鸡萝丝出门去散步，狐狸跟在后面想抓她。但每次狐狸都倒霉——被钉耙砸到头、埋进小麦堆、被蜜蜂追……萝丝始终不知道，继续优雅地走回家。',
      howToTell: '讲萝丝的故事（很少字）时用轻松悠闲的语气，讲狐狸的故事（画面细节）时夸张倒霉的样子。',
      themes: ['观察力', '幽默', '农场'],
      tips: '这个故事有一半的故事在画面里，要仔细看每个细节才有趣。' },
    { name: '月亮说晚安', author: 'Margaret Wise Brown', ageRange: [12,18], duration: '3分钟', type: '睡前故事',
      description: '月亮在天上对每一个东西说晚安——小兔子、小熊、小老鼠……全世界都安静下来，该睡觉了。',
      howToTell: '用非常轻柔温柔的声音读，每说一个"晚安"就让宝宝也轻轻地说"晚安"。',
      themes: ['睡前', '安抚', '晚安仪式'],
      tips: '非常适合睡前读，帮助宝宝建立睡前仪式。' },
    { name: '小鸡球球系列', author: '入山智', ageRange: [12,18], duration: '3分钟/本', type: '翻翻书',
      description: '小鸡球球是一只小黄鸡，和朋友们一起玩、一起探险的故事。有翻翻页、立体页。',
      howToTell: '翻翻页让宝宝来翻，立体页打开时配合惊喜的表情。球球的叫声"叽叽叽"可以一起模仿。',
      themes: ['友情', '探险', '成长'],
      tips: '系列有多本，适合反复阅读。' },
    // 18-24月龄
    { name: '彩虹色的花', author: '麦克・格雷涅茨', ageRange: [18,24], duration: '5分钟', type: '品格绘本',
      description: '一朵彩虹色的花，把自己的花瓣一片一片送给需要帮助的小动物：帮蚂蚁过河、给老鼠当扇子、给刺猬当披肩……最后花瓣全部没了，冬天来了。',
      howToTell: '每送出一片花瓣都停顿一下，说"这是谁需要呢？"→揭示答案→"彩虹色的花把花瓣送给了它"。',
      themes: ['分享', '助人', '生命轮回'],
      tips: '告诉宝宝分享的意义，但不要道德说教。' },
    { name: '獾的礼物', author: '苏珊・华莱', ageRange: [18,24], duration: '5分钟', type: '生命教育',
      description: '獾爷爷死了，但他教会了动物们很多事情。鼹鼠学会了剪纸、青蛙学会了滑冰、狐狸学会了系领带……大家想念獾爷爷。',
      howToTell: '平静温柔地讲述，不要太悲伤。这是帮助宝宝理解"死亡"和"留下"的概念。',
      themes: ['离别', '感恩', '生命教育'],
      tips: '可能需要解释"獾爷爷去哪里了"，根据宝宝的反应来决定讲多少。' },
    { name: '14只老鼠系列', author: '岩村和朗', ageRange: [18,24], duration: '5分钟/本', type: '自然绘本',
      description: '14只老鼠是一个大家庭，它们一起挖山药、搭帐篷、捣年糕、赏月……每一本都是对自然的描绘和对家庭生活的热爱。',
      howToTell: '数一数每页有几只老鼠，找找老鼠们藏在哪儿。观察画面里的植物、昆虫、小动物。',
      themes: ['家庭', '自然', '合作'],
      tips: '适合反复看，每次都能发现新细节。' },
    { name: '花婆婆', author: '芭芭拉・库尼', ageRange: [18,24], duration: '5分钟', type: '品格绘本',
      description: '小女孩答应爷爷长大后做三件事：去很远的地方旅行、住在海边、做让世界变得更美丽的事。',
      howToTell: '问宝宝"她做了什么事让世界变美？"→"你也想让世界变美吗？"→"我们可以做什么？"',
      themes: ['梦想', '行动力', '美丽'],
      tips: '在宝宝心里种下"让世界变美"的种子。' },
    { name: '巴巴伯系列', author: 'Eric Burnet', ageRange: [18,24], duration: '3分钟/本', type: '幽默绘本',
      description: '巴巴伯是一只大猩猩，做各种有趣的事：在头发里种花、把自己变成雪人、找不到妈妈着急大哭……',
      howToTell: '巴巴伯的各种夸张表情和动作都表演出来。让宝宝找找巴巴伯在哪里。',
      themes: ['幽默', '想象', '日常生活'],
      tips: '画风独特，幽默感强，是那种"看过就会记住"的书。' },
    // 2-3岁
    { name: '大卫不可以系列', author: 'David Shannon', ageRange: [24,36], duration: '3分钟', type: '行为绘本',
      description: '大卫总是做"不可以"的事：站在椅子上够饼干、在家里玩棒球、打翻浴缸的水……但最后妈妈总是说"大卫，我爱你！"',
      howToTell: '大卫做"坏事"时用"大卫不可以！"的夸张语气，最后用最温柔的声音说"我爱你"。',
      themes: ['规则', '行为边界', '无条件的爱'],
      tips: '宝宝会特别喜欢大卫的"调皮"，因为那就是他们想做的事。不要用大卫当反面教材。' },
    { name: '牙齿大街的新鲜事', author: '安娜・鲁斯曼', ageRange: [24,36], duration: '5分钟', type: '科普绘本',
      description: '哈克和迪克是两个小精灵，在牙齿里建房子、储存糖果。但他们被牙医发现了……',
      howToTell: '配合手势表演两个小精灵在牙齿里忙碌的样子。讲到牙医时一起"啊——"张开嘴。',
      themes: ['牙齿卫生', '口腔健康', '科普'],
      tips: '看完这本书宝宝通常会愿意刷牙，因为不想让哈克迪克在牙齿里安家。' },
    { name: '肚子里有个火车站', author: '安娜・鲁斯曼', ageRange: [24,36], duration: '5分钟', type: '科普绘本',
      description: '小女孩朱莉娅吃得太快太多，小精灵们罢工了，肚子里的小火车也停开了……',
      howToTell: '用游戏的方式："小精灵们喜欢什么样的食物？"→"小精灵们不喜欢什么？"→"我们吃下去的东西是怎么变成营养的？"',
      themes: ['饮食习惯', '消化系统', '科普'],
      tips: '帮助宝宝理解为什么要细嚼慢咽。' },
    { name: '天空100层的房子', author: '岩井俊雄', ageRange: [24,36], duration: '8分钟', type: '想象力绘本',
      description: '一个小男孩向日葵的种子出发去天空旅行，每10层住着不同的动物（云猫、天空鼠、天马、独角兽……）一直到100层。',
      howToTell: '每翻一页数一数是第几层，是什么动物在干什么。观察画面细节：动物们的生活用品、窗外风景。',
      themes: ['想象力', '数数', '自然'],
      tips: '系列还有《地下100层的房子》《海底100层的房子》，宝宝会反复要求读。' },
    { name: '世界上最棒的爷爷', author: 'Neil Gaiman', ageRange: [24,36], duration: '5分钟', type: '亲情绘本',
      description: '小女孩问爷爷各种关于过去的问题，爷爷用故事来回答。故事越讲越长，越来越奇幻……',
      howToTell: '每个故事用不同的语气讲：海的故事是蓝色的调子，丛林故事是紧张的……',
      themes: ['亲情', '想象力', '代际关系'],
      tips: '适合有祖辈疼爱的宝宝，也适合和爷爷奶奶一起读。' },
    { name: '我不敢，我能做到', author: 'Jez Alborough', ageRange: [24,36], duration: '3分钟', type: '勇气绘本',
      description: '小猩猩Eddie总说"我不敢"，但其实它能做的事情比它以为的多得多。',
      howToTell: 'Eddie说"我不敢"时用害怕的声音讲，Eddie成功时用骄傲的声音讲。然后问宝宝"你有什么是原来不敢，后来做到的？"',
      themes: ['勇气', '自信', '克服恐惧'],
      tips: '帮助宝宝建立"我可以做到"的信念。' }
  ];

  // ===================== 作息模板 =====================
  var routines = {
    '6-12': {
      wake: '07:00', sleep: '20:00',
      schedule: [
        { time: '07:00-07:30', activity: '起床+洗漱', parentTips: '用轻柔的方式唤醒，如拉开窗帘说"早上好"。按顺序做：换尿布→洗脸→擦香香→穿衣。',
          expandable: { type: 'routine', title: '起床流程', steps: ['拉开窗帘，自然光唤醒，"早上好！"', '换尿布/如厕训练', '用柔软的纱布巾擦脸', '涂抹婴儿面霜', '穿衣服，让宝宝参与（如"伸左手"）'] }},
        { time: '07:30-08:00', activity: '早餐（奶）', parentTips: '继续按需喂养母乳或配方奶。6月龄后可开始尝试辅食。',
          expandable: { type: 'recipe', title: '今日早餐' }},
        { time: '08:00-10:00', activity: '亲子游戏时间', parentTips: '每天至少30分钟高质量陪伴。放下手机，和宝宝一起玩。',
          expandable: { type: 'game', title: '今日推荐游戏', description: '适合6-8月龄：镜子里的宝宝、积木敲敲乐。' }},
        { time: '10:00-11:00', activity: '户外活动', parentTips: '每天至少1小时户外活动。晒太阳（露出手臂/腿），促进维生素D合成。',
          expandable: { type: 'outdoor', title: '户外活动建议', description: '去公园散步、在小区晒太阳、看看花草树木和小动物。' }},
        { time: '11:00-12:00', activity: '午餐（奶+辅食）', parentTips: '先喂奶，半饱后再尝试辅食。不要强迫，以探索为主。',
          expandable: { type: 'recipe', title: '今日午餐' }},
        { time: '12:00-14:00', activity: '午睡', parentTips: '建立固定的午睡仪式：拉窗帘→放轻柔音乐→说"该睡觉了"。',
          expandable: { type: 'sleep', title: '午睡建议', description: '这个阶段午睡1-2次，每次1-2小时。别强求，让宝宝自然入睡。' }},
        { time: '14:00-15:00', activity: '起床+水果时间', parentTips: '可以给少量水果泥，如苹果泥、香蕉泥。',
          expandable: { type: 'snack', title: '水果推荐' }},
        { time: '15:00-16:30', activity: '室内活动/亲子互动', parentTips: '天气不好时在室内玩藏猫猫、拍手游戏、读布书。',
          expandable: { type: 'game', title: '室内游戏' }},
        { time: '16:30-18:00', activity: '户外活动', parentTips: '傍晚的户外时光，看看夕阳和小动物。',
          expandable: { type: 'outdoor', title: '傍晚户外' }},
        { time: '18:00-19:00', activity: '晚餐（奶+辅食）', parentTips: '辅食量可以比午餐多一些。',
          expandable: { type: 'recipe', title: '今日晚餐' }},
        { time: '19:00-20:00', activity: '洗澡+亲子时光', parentTips: '洗澡时玩水是宝宝最开心的时光。洗完澡读几页布书。',
          expandable: { type: 'bath', title: '洗澡流程', steps: ['调好水温（38°C左右）', '从脚慢慢放入水，先洗脸再洗头', '用柔软的毛巾擦洗身体各部位', '玩具时间：让宝宝自己拍水', '出浴后立即擦干，涂抹润肤露', '穿上睡袋，准备入睡'] }},
        { time: '20:00', activity: '入睡', parentTips: '建立睡前仪式：洗澡→抚触→穿睡袋→关灯→唱摇篮曲。不要开灯陪玩。' }
      ]
    },
    '12-18': {
      wake: '07:30', sleep: '20:30',
      schedule: [
        { time: '07:30-08:00', activity: '起床+洗漱', parentTips: '培养固定作息。可以用"刷牙歌"让刷牙变得有趣。',
          expandable: { type: 'routine', title: '起床流程', steps: ['叫醒："新的一天开始了！"', '去洗手间，教宝宝坐小马桶', '刷牙：示范→让宝宝自己刷→家长再刷一遍', '洗手洗脸', '穿衣服（让宝宝自己选择）'] }},
        { time: '08:00-08:30', activity: '早餐', parentTips: '让宝宝自己用勺子吃，即使弄脏也没关系。鼓励自主进食。',
          expandable: { type: 'recipe', title: '今日早餐' }},
        { time: '08:30-10:00', activity: '自由玩耍', parentTips: '宝宝自由探索的时间，家长在旁陪伴观察，不主动干预。',
          expandable: { type: 'game', title: '自由探索' }},
        { time: '10:00-10:30', activity: '水果点心', parentTips: '固定在两餐之间给点心，不要随要随给。',
          expandable: { type: 'snack', title: '健康点心' }},
        { time: '10:30-12:00', activity: '户外活动', parentTips: '每天至少2小时户外。跑跑跳跳，消耗体力。',
          expandable: { type: 'outdoor', title: '户外活动' }},
        { time: '12:00-12:30', activity: '午餐', parentTips: '食物切成适合手抓的大小，继续鼓励自主进食。',
          expandable: { type: 'recipe', title: '今日午餐' }},
        { time: '12:30-14:30', activity: '午睡', parentTips: '午睡前不要玩太兴奋的游戏。建立固定的睡前仪式。',
          expandable: { type: 'sleep', title: '午睡建议' }},
        { time: '14:30-15:00', activity: '起床+下午点心', parentTips: '点心以健康为主：水果、酸奶、小饼干。',
          expandable: { type: 'snack', title: '下午点心' }},
        { time: '15:00-16:30', activity: '亲子游戏/早教', parentTips: '选择适龄的游戏，寓教于乐。',
          expandable: { type: 'game', title: '今日推荐游戏' }},
        { time: '16:30-18:00', activity: '户外活动', parentTips: '傍晚户外可以带宝宝去小区找同龄小伙伴玩。',
          expandable: { type: 'outdoor', title: '傍晚户外' }},
        { time: '18:00-18:30', activity: '晚餐', parentTips: '全家一起吃饭，营造好的用餐氛围。',
          expandable: { type: 'recipe', title: '今日晚餐' }},
        { time: '18:30-19:00', activity: '亲子时光', parentTips: '玩一些安静的游戏，不要太兴奋。',
          expandable: { type: 'game', title: '安静游戏' }},
        { time: '19:00-19:30', activity: '洗澡', parentTips: '洗澡时间可以玩水，但不要超过15分钟。',
          expandable: { type: 'bath', title: '洗澡建议' }},
        { time: '19:30-20:00', activity: '睡前故事', parentTips: '选择2-3本绘本，家长讲给宝宝听。',
          expandable: { type: 'story', title: '今晚故事推荐' }},
        { time: '20:00-20:30', activity: '入睡', parentTips: '关灯，建立"现在是睡觉时间"的信号。' }
      ]
    },
    '18-24': {
      wake: '08:00', sleep: '20:30',
      schedule: [
        { time: '08:00-08:30', activity: '起床+早餐', parentTips: '和宝宝一起准备早餐，参与感让吃饭更香。',
          expandable: { type: 'recipe', title: '今日早餐' }},
        { time: '09:00-10:30', activity: '户外/亲子游戏', parentTips: '1-2小时户外活动，跑跳、踢球、玩沙。',
          expandable: { type: 'game', title: '今日推荐游戏' }},
        { time: '10:30-11:00', activity: '水果点心时间', parentTips: '和宝宝一起洗水果，增加参与感。',
          expandable: { type: 'snack', title: '水果时间' }},
        { time: '11:00-12:00', activity: '室内早教', parentTips: '读绘本、拼图、过家家等安静游戏。',
          expandable: { type: 'game', title: '早教游戏' }},
        { time: '12:00-12:30', activity: '午餐', parentTips: '可以开始用儿童餐具，让宝宝练习用勺子。',
          expandable: { type: 'recipe', title: '今日午餐' }},
        { time: '12:30-14:30', activity: '午睡', parentTips: '继续午睡习惯，睡醒后情绪更稳定。',
          expandable: { type: 'sleep', title: '午睡建议' }},
        { time: '14:30-15:00', activity: '起床+下午茶', parentTips: '可以是酸奶+水果的组合。',
          expandable: { type: 'snack', title: '下午茶' }},
        { time: '15:00-16:30', activity: '户外活动', parentTips: '每天保持2小时户外，接近大自然。',
          expandable: { type: 'outdoor', title: '户外活动' }},
        { time: '16:30-18:00', activity: '亲子时光', parentTips: '晚饭前的高质量陪伴时间。',
          expandable: { type: 'game', title: '亲子游戏' }},
        { time: '18:00-18:30', activity: '晚餐', parentTips: '全家围坐一起吃，让宝宝参与摆碗筷。',
          expandable: { type: 'recipe', title: '今日晚餐' }},
        { time: '18:30-19:00', activity: '洗澡', parentTips: '可以开始教宝宝认识身体部位。',
          expandable: { type: 'bath', title: '洗澡建议' }},
        { time: '19:00-20:00', activity: '睡前故事', parentTips: '开始引入有情节的故事绘本。',
          expandable: { type: 'story', title: '今晚故事推荐' }},
        { time: '20:00-20:30', activity: '入睡准备', parentTips: '刷牙→换睡衣→上厕所→关灯→说晚安。' }
      ]
    },
    '24-36': {
      wake: '07:30', sleep: '21:00',
      schedule: [
        { time: '07:30-08:00', activity: '起床+早餐', parentTips: '可以开始教宝宝自己穿简单的衣服（如套头衫）。',
          expandable: { type: 'recipe', title: '今日早餐' }},
        { time: '08:00-09:00', activity: '准备出门', parentTips: '2岁后可以参与收纳玩具、准备出门物品。',
          expandable: { type: 'routine', title: '出门准备' }},
        { time: '09:00-11:00', activity: '户外活动', parentTips: '踢球、骑平衡车、在公园和同龄孩子玩。',
          expandable: { type: 'outdoor', title: '户外活动' }},
        { time: '11:00-12:00', activity: '回家+午餐准备', parentTips: '让宝宝帮忙洗菜、摆碗筷。',
          expandable: { type: 'recipe', title: '今日午餐' }},
        { time: '12:00-12:30', activity: '午餐', parentTips: '可以尝试用筷子（先从儿童筷开始）。',
          expandable: { type: 'recipe', title: '今日午餐' }},
        { time: '12:30-15:00', activity: '午睡', parentTips: '2岁后很多孩子只睡下午的午觉了。',
          expandable: { type: 'sleep', title: '午睡建议' }},
        { time: '15:00-15:30', activity: '下午茶', parentTips: '水果、酸奶、小点心。',
          expandable: { type: 'snack', title: '下午茶' }},
        { time: '15:30-17:00', activity: '室内活动/早教', parentTips: '拼图、积木、涂色、角色扮演。',
          expandable: { type: 'game', title: '今日推荐游戏' }},
        { time: '17:00-18:00', activity: '户外活动', parentTips: '傍晚散步，和邻居孩子玩。',
          expandable: { type: 'outdoor', title: '傍晚户外' }},
        { time: '18:00-18:30', activity: '晚餐', parentTips: '全家一起吃，可以聊一聊今天发生的事。',
          expandable: { type: 'recipe', title: '今日晚餐' }},
        { time: '18:30-19:00', activity: '家庭时间', parentTips: '全家一起玩游戏、讲故事。',
          expandable: { type: 'game', title: '家庭游戏' }},
        { time: '19:00-19:30', activity: '洗澡', parentTips: '可以开始教宝宝自己洗澡（在家长的监督下）。',
          expandable: { type: 'bath', title: '洗澡建议' }},
        { time: '19:30-20:00', activity: '睡前故事', parentTips: '可以问宝宝"你想听什么故事？"让他做选择。',
          expandable: { type: 'story', title: '今晚故事推荐' }},
        { time: '20:00-21:00', activity: '入睡', parentTips: '建立固定的睡前仪式，这个阶段可以开始"terrible two"，家长要有耐心。' }
      ]
    }
  };

  // ===================== 家长时间 =====================
  var parentTime = [
    {
      category: '孩子睡着后你可以干嘛',
      activities: [
        { name: '整理家务', duration: '20分钟', description: '趁孩子睡着把玩具收好、衣服叠好、厨房收拾干净。做个"快速家务清单"，10-20分钟搞定。' },
        { name: '自我提升', duration: '30分钟', description: '看书/学技能/听播客/看线上课程。哪怕每天只有30分钟，一年也是180+小时。' },
        { name: '休息恢复', duration: '20分钟', description: '补个觉（如果你也累了）、刷手机放松、泡杯茶/咖啡坐在阳台发发呆。这不是浪费时间，是必要的恢复。' },
        { name: '规划第二天', duration: '10分钟', description: '想想明天要准备什么食材、穿什么衣服、有什么重要的事提前安排好。有计划让第二天从容很多。' },
        { name: '夫妻/个人时间', duration: '不固定', description: '孩子睡着后是真正属于自己的时间。可以和伴侣聊聊天，也可以单纯享受独处。' },
        { name: '健康护理', duration: '15分钟', description: '敷面膜、做简单拉伸、泡脚。照顾好自己的身心，才能更好地照顾孩子。' }
      ]
    },
    {
      category: '周末可以和孩子一起做的事',
      activities: [
        { name: '一起做饭', duration: '1-2小时', description: '让孩子参与洗菜、搅拌、摆盘。2岁后可以帮忙揉面团、包饺子。这是最真实的早教。' },
        { name: '户外探索', duration: '半天', description: '去公园、动物园、农场、博物馆。让孩子接触大自然和真实世界。' },
        { name: '亲子阅读时间', duration: '30分钟', description: '平时工作日可能比较赶，周末可以好好读几本绘本，享受亲子时光。' },
        { name: '艺术创作', duration: '1小时', description: '手指画、捏黏土、贴贴纸、做手工。不追求结果，享受过程。' },
        { name: '整理照片', duration: '30分钟', description: '把孩子的照片整理一下，冲洗出来做相册。让孩子一起看，一起回忆。' }
      ]
    },
    {
      category: '给自己的一点时间（哪怕每天5分钟）',
      activities: [
        { name: '冥想或深呼吸', duration: '5分钟', description: '如果感到焦虑或疲惫，闭上眼睛深呼吸。花5分钟让自己平静下来。' },
        { name: '写日记', duration: '5-10分钟', description: '记录孩子的成长瞬间，也记录自己的感受。若干年后回看，是珍贵的回忆。' },
        { name: '散步', duration: '15分钟', description: '自己一个人出门走一走，不需要去哪里，就是走一走。' },
        { name: '听一首喜欢的歌', duration: '5分钟', description: '不要快进，不要切歌，就完整地听一首歌。让自己从"妈妈模式"切换一下。' }
      ]
    }
  ];

  // ===================== 国家标准 =====================
  var references = [
    {
      title: '0-6岁儿童喂养指南（2022版）',
      source: '国家卫生健康委员会',
      summary: '核心建议：6月龄内纯母乳喂养；6月龄起添加辅食，从富铁泥糊状食物开始；辅食不加调味品；继续母乳喂养至2岁或以上。',
      url: ''
    },
    {
      title: '0-2岁体格发育评价标准',
      source: 'WHO',
      summary: '通过身高、体重、头围等指标监测儿童生长发育曲线，关注生长速度而非绝对值。',
      url: ''
    },
    {
      title: '儿童心理行为发育预警征象',
      source: '国家卫生健康委员会',
      summary: '列出各年龄段需要关注的发育异常信号，如3月龄不会抬头、6月龄不会笑出声、1岁不会独站等。',
      url: ''
    },
    {
      title: '儿童口腔保健',
      source: '中华口腔医学会',
      summary: '第一颗乳牙萌出后就要开始刷牙，使用儿童含氟牙膏，3岁前牙膏用量米粒大小。',
      url: ''
    }
  ];

  // ===================== 辅助函数 =====================
  function getAgeRange(months) {
    if (months < 6) return '0-6';
    if (months < 12) return '6-12';
    if (months < 18) return '12-18';
    if (months < 24) return '18-24';
    return '24-36';
  }

  function getRoutineForChild(months) {
    var range = getAgeRange(months);
    return routines[range] || routines['24-36'];
  }

  // ===================== 公开 API =====================
  return {
    // 获取适合月龄的食谱
    getRecipes: function(ageMonths, mealType) {
      var range = getAgeRange(ageMonths);
      var all = recipes[range] || recipes['24-36'];
      if (!mealType) return all;
      return all.filter(function(r) {
        for (var i = 0; i < r.meals.length; i++) {
          if (r.meals[i].time.indexOf(mealType) !== -1) return true;
        }
        return false;
      });
    },

    // 获取适合的游戏
    getGames: function(ageMonths, type) {
      var min = ageMonths - 3;
      var max = ageMonths + 6;
      var filtered = games.filter(function(g) {
        return g.ageRange[0] <= max && g.ageRange[1] >= min;
      });
      if (type) {
        filtered = filtered.filter(function(g) { return g.type === type; });
      }
      return filtered;
    },

    // 获取适合的故事
    getStories: function(ageMonths) {
      var min = ageMonths - 3;
      var max = ageMonths + 12;
      return stories.filter(function(s) {
        return s.ageRange[0] <= max && s.ageRange[1] >= min;
      });
    },

    // 获取今日一句话总结
    getTodaySummary: function(child) {
      var months = child.months || 24;
      var name = child.name || '宝宝';
      var summaries = [
        name + '现在处于语言爆发期，多和宝宝说话可以促进语言发育。',
        name + '正处于大运动发展期，每天保证足够的爬行/走路时间很重要。',
        name + '现在是培养自主进食的好时机，让宝宝自己吃，虽然会弄得很乱。',
        name + '这个阶段宝宝好奇心很强，多带出去探索吧！',
        name + '如厕训练可以从现在开始准备了，观察宝宝的排便规律。'
      ];
      // 根据关注点调整
      if (child.concerns) {
        if (child.concerns.indexOf('睡眠') !== -1) {
          summaries.unshift('睡眠是孩子成长的关键，今天注意观察睡眠信号，及时哄睡。');
        }
        if (child.concerns.indexOf('喂养') !== -1) {
          summaries.unshiftshift('辅食添加期，注意观察是否有过敏反应，每次只加一种新食材。');
        }
      }
      // 随机选一条
      var idx = Math.floor(Math.random() * summaries.length);
      return summaries[idx];
    },

    // 获取当天作息计划
    getDailyPlan: function(child, date) {
      var months = child.months || 24;
      var routine = getRoutineForChild(months);
      var result = {
        wake: routine.wake,
        sleep: routine.sleep,
        schedule: []
      };

      for (var i = 0; i < routine.schedule.length; i++) {
        var item = routine.schedule[i];
        var exp = item.expandable || {};
        var expContent = null;

        if (exp.type === 'recipe') {
          var ageRange = getAgeRange(months);
          var rlist = recipes[ageRange] || recipes['24-36'];
          var ridx = Math.floor(Math.random() * rlist.length);
          var recipe = rlist[ridx];
          var meal = recipe.meals[Math.floor(Math.random() * recipe.meals.length)];
          expContent = {
            type: 'recipe',
            title: meal.name,
            ingredients: meal.ingredients,
            steps: meal.steps,
            tips: meal.tips,
            nutrition: meal.nutrition
          };
        } else if (exp.type === 'game') {
          var min = months - 3;
          var max = months + 6;
          var availGames = games.filter(function(g) {
            return g.ageRange[0] <= max && g.ageRange[1] >= min;
          });
          if (availGames.length > 0) {
            var gidx = Math.floor(Math.random() * availGames.length);
            expContent = {
              type: 'game',
              title: availGames[gidx].name,
              duration: availGames[gidx].duration,
              materials: availGames[gidx].materials,
              steps: availGames[gidx].steps,
              benefits: availGames[gidx].benefits,
              tips: availGames[gidx].tips
            };
          }
        } else if (exp.type === 'story') {
          var minS = months - 3;
          var maxS = months + 12;
          var availStories = stories.filter(function(s) {
            return s.ageRange[0] <= maxS && s.ageRange[1] >= minS;
          });
          if (availStories.length > 0) {
            var sidx = Math.floor(Math.random() * availStories.length);
            expContent = {
              type: 'story',
              title: availStories[sidx].name,
              duration: availStories[sidx].duration,
              description: availStories[sidx].description,
              howToTell: availStories[sidx].howToTell,
              themes: availStories[sidx].themes
            };
          }
        }

        result.schedule.push({
          time: item.time,
          activity: item.activity,
          parentTips: item.parentTips,
          expandable: expContent
        });
      }

      return result;
    },

    // 获取家长时间建议
    getParentTime: function(child) {
      return parentTime;
    },

    // 获取国家标准
    getReferences: function() {
      return references;
    },

    // 搜索食谱
    searchRecipes: function(query, ageMonths) {
      var range = getAgeRange(ageMonths);
      var all = recipes[range] || recipes['24-36'];
      var q = query.toLowerCase();
      return all.filter(function(r) {
        return r.name.toLowerCase().indexOf(q) !== -1 ||
               r.tags.some(function(t) { return t.toLowerCase().indexOf(q) !== -1; });
      });
    },

    // 获取三餐食谱
    getMealPlan: function(ageMonths, date) {
      var range = getAgeRange(ageMonths);
      var rlist = recipes[range] || recipes['24-36'];
      var result = {};
      var mealTimes = ['早餐', '午餐', '晚餐', '点心'];
      for (var i = 0; i < mealTimes.length; i++) {
        var filtered = rlist.filter(function(r) {
          return r.meals.some(function(m) { return m.time === mealTimes[i]; });
        });
        if (filtered.length > 0) {
          var r = filtered[Math.floor(Math.random() * filtered.length)];
          var m = r.meals.filter(function(m2) { return m2.time === mealTimes[i]; })[0];
          result[mealTimes[i]] = { recipe: r, meal: m };
        }
      }
      return result;
    },

    // ===================== 发育里程碑 =====================
    getMilestones: function(ageMonths) {
      var all = [
        // 0-3个月
        {id:'m_0_1', month:0, category:'大运动', title:'抬头', description:'俯卧时能抬头片刻', tips:'每天清醒时趴着练习几分钟'},
        {id:'m_0_2', month:1, category:'大运动', title:'转头', description:'能转头寻找声源', tips:'用沙锤在两侧引导'},
        {id:'m_0_3', month:2, category:'大运动', title:'抬胸', description:'俯卧时可抬头45度', tips:'用黑白卡在前方吸引'},
        {id:'m_0_4', month:2, category:'社交', title:'社会性微笑', description:'对逗引会微笑回应', tips:'多与宝宝面对面互动'},
        {id:'m_0_5', month:3, category:'大运动', title:'翻身', description:'能从仰卧翻到侧卧', tips:'用玩具在侧面引逗'},
        {id:'m_0_6', month:3, category:'语言', title:'咿呀声', description:'能发出咿咿呀呀的声音', tips:'模仿宝宝的声音回应'},
        // 3-6个月
        {id:'m_3_1', month:4, category:'大运动', title:'翻身', description:'能从仰卧翻到俯卧', tips:'穿着方便活动的衣物练习'},
        {id:'m_3_2', month:5, category:'精细动作', title:'抓握', description:'能主动抓握玩具', tips:'提供不同材质的玩具'},
        {id:'m_3_3', month:5, category:'认知', title:'认母', description:'能认出妈妈，开始认生', tips:'多和主要照护者互动'},
        {id:'m_3_4', month:6, category:'大运动', title:'靠坐', description:'能独坐片刻（需辅助）', tips:'用枕头围成一圈保护'},
        {id:'m_3_5', month:6, category:'语言', title:'辅音', description:'能发出ba、ma等音', tips:'经常和宝宝说话'},
        // 6-9个月
        {id:'m_6_1', month:7, category:'大运动', title:'爬行', description:'手膝着地爬行，可后退', tips:'用玩具在前方引导'},
        {id:'m_6_2', month:7, category:'社交', title:'认生期', description:'对陌生人产生警惕哭闹', tips:'不要强迫亲近陌生人'},
        {id:'m_6_3', month:8, category:'精细动作', title:'捏取', description:'能用拇指食指捏起小东西', tips:'提供安全的小零食练习'},
        {id:'m_6_4', month:8, category:'语言', title:'无意识叫爸妈', description:'发baba、mama音', tips:'多教宝宝认识家庭成员'},
        {id:'m_6_5', month:9, category:'大运动', title:'扶站', description:'扶着家具或大人手走路', tips:'确保环境安全'},
        {id:'m_6_6', month:9, category:'社交', title:'挥手再见', description:'会模仿挥手再见', tips:'日常生活中多练习'},
        // 9-12个月
        {id:'m_9_1', month:10, category:'大运动', title:'独站', description:'独站片刻，不扶东西', tips:'和宝宝玩拉起蹲下游戏'},
        {id:'m_9_2', month:10, category:'社交', title:'分离焦虑', description:'主要照护者离开时哭闹', tips:'正式告别，不要偷偷离开'},
        {id:'m_9_3', month:11, category:'精细动作', title:'拇食指捏', description:'熟练使用拇食指捏取', tips:'玩捡豆子等游戏'},
        {id:'m_9_4', month:12, category:'大运动', title:'独走', description:'独走几步到十几步', tips:'允许跌倒，不要过度保护'},
        {id:'m_9_5', month:12, category:'语言', title:'有意识叫爸妈', description:'叫爸妈是有意义的', tips:'指认家庭成员并告诉称呼'},
        // 12-18个月
        {id:'m_12_1', month:13, category:'大运动', title:'独走稳', description:'走路越来越稳', tips:'多到户外练习'},
        {id:'m_12_2', month:14, category:'精细动作', title:'叠积木', description:'能叠2-3块积木', tips:'提供轻便的积木'},
        {id:'m_12_3', month:15, category:'语言', title:'说单词', description:'能说10-20个单词', tips:'指物命名练习'},
        {id:'m_12_4', month:18, category:'认知', title:'指认身体', description:'能指认身体部位', tips:'边指边说身体部位名称'},
        {id:'m_12_5', month:18, category:'社交', title:'平行游戏', description:'开始与其他孩子互动', tips:'多带孩子去游乐场'},
        // 18-24个月
        {id:'m_18_1', month:20, category:'语言', title:'说短语', description:'能说2-3个词的短语', tips:'描述正在做的事情'},
        {id:'m_18_2', month:21, category:'大运动', title:'跑', description:'能跑但不稳', tips:'在安全环境里追跑游戏'},
        {id:'m_18_3', month:22, category:'精细动作', title:'自己吃饭', description:'能用勺子自己吃饭', tips:'允许弄脏，允许自己来'},
        {id:'m_18_4', month:24, category:'语言', title:'说句子', description:'能说简单句子', tips:'多读绘本，复述故事'},
        // 24-36个月
        {id:'m_24_1', month:24, category:'认知', title:'假想游戏', description:'会抱着娃娃假装喂食', tips:'提供娃娃和道具'},
        {id:'m_24_2', month:30, category:'社交', title:'合作游戏', description:'能和其他孩子合作', tips:'组织简单的合作游戏'},
        {id:'m_24_3', month:36, category:'语言', title:'讲故事', description:'能讲简单故事', tips:'多读绘本，鼓励复述'},
        {id:'m_24_4', month:36, category:'认知', title:'认颜色', description:'能认识基本颜色', tips:'生活中随时指认颜色'}
      ];
      
      // 过滤：返回当前月龄及之前6个月内的里程碑
      var cutoff = ageMonths;
      return all.filter(function(m) { return m.month <= cutoff; });
    }

    // ===================== WHO 生长曲线标准 (0-60个月) =====================
    , getWhoWeightBoys: function() {
      // [月龄, P3, P15, P50, P85, P97] 单位: kg
      return [
        [0,2.5,2.9,3.3,3.9,4.4],[1,3.4,3.9,4.5,5.1,5.8],[2,4.3,4.9,5.6,6.3,7.1],
        [3,5.0,5.7,6.4,7.2,8.0],[4,5.6,6.3,7.0,7.9,8.8],[5,6.0,6.9,7.5,8.5,9.5],
        [6,6.4,7.1,7.9,8.9,10.0],[7,6.7,7.4,8.3,9.3,10.5],[8,6.9,7.7,8.6,9.7,10.9],
        [9,7.1,8.0,8.9,10.0,11.3],[10,7.4,8.2,9.2,10.3,11.6],[11,7.6,8.4,9.4,10.5,11.9],
        [12,7.7,8.6,9.6,10.8,12.2],[13,7.9,8.8,9.9,11.0,12.5],[14,8.1,9.0,10.1,11.3,12.8],
        [15,8.3,9.2,10.3,11.5,13.1],[16,8.4,9.4,10.5,11.8,13.4],[17,8.6,9.6,10.7,12.0,13.6],
        [18,8.8,9.8,10.9,12.2,13.9],[19,8.9,10.0,11.1,12.5,14.2],[20,9.1,10.1,11.3,12.7,14.5],
        [21,9.2,10.3,11.5,12.9,14.7],[22,9.4,10.5,11.7,13.1,15.0],[23,9.5,10.6,11.8,13.3,15.2],
        [24,9.7,10.8,12.0,13.5,15.5],[27,10.2,11.4,12.7,14.3,16.4],[30,10.7,11.9,13.3,15.0,17.2],
        [33,11.1,12.4,13.9,15.6,18.1],[36,11.5,12.9,14.4,16.2,18.9],[42,12.3,13.8,15.5,17.5,20.5],
        [48,13.0,14.6,16.5,18.6,21.9],[54,13.7,15.4,17.5,19.8,23.4],[60,14.4,16.3,18.6,21.1,25.0]
      ];
    }
    , getWhoWeightGirls: function() {
      return [
        [0,2.4,2.8,3.2,3.7,4.2],[1,3.2,3.6,4.2,4.8,5.5],[2,3.9,4.5,5.1,5.8,6.6],
        [3,4.5,5.2,5.8,6.6,7.5],[4,5.0,5.7,6.4,7.3,8.2],[5,5.4,6.1,6.9,7.8,8.8],
        [6,5.7,6.5,7.3,8.2,9.3],[7,6.0,6.8,7.6,8.6,9.8],[8,6.3,7.0,7.9,9.0,10.2],
        [9,6.5,7.3,8.2,9.3,10.6],[10,6.7,7.5,8.5,9.6,11.0],[11,6.9,7.7,8.7,9.9,11.4],
        [12,7.0,7.9,8.9,10.1,11.7],[13,7.2,8.1,9.2,10.4,12.0],[14,7.4,8.3,9.4,10.6,12.3],
        [15,7.6,8.5,9.6,10.9,12.6],[16,7.7,8.7,9.8,11.1,12.9],[17,7.9,8.9,10.0,11.4,13.2],
        [18,8.1,9.1,10.2,11.6,13.5],[19,8.2,9.2,10.4,11.8,13.8],[20,8.4,9.4,10.6,12.1,14.1],
        [21,8.6,9.6,10.9,12.3,14.4],[22,8.7,9.8,11.1,12.5,14.7],[23,8.9,10.0,11.3,12.8,15.0],
        [24,9.0,10.2,11.5,13.0,15.4],[27,9.5,10.7,12.1,13.7,16.2],[30,9.9,11.2,12.7,14.4,17.1],
        [33,10.3,11.7,13.3,15.1,18.0],[36,10.7,12.1,13.9,15.8,19.0],[42,11.4,13.0,15.0,17.1,20.8],
        [48,12.1,13.9,16.1,18.5,22.7],[54,12.7,14.7,17.2,19.8,24.6],[60,13.4,15.6,18.2,21.2,26.5]
      ];
    }
    , getWhoHeightBoys: function() {
      // [月龄, P3, P50, P97] 单位: cm
      return [
        [0,46.1,50.4,54.7],[1,51.1,54.7,58.4],[2,54.7,58.4,62.2],[3,57.6,61.4,65.1],
        [4,60.0,63.9,67.7],[5,61.9,65.9,70.0],[6,63.6,67.6,71.6],[7,65.1,69.2,73.3],
        [8,66.5,70.6,74.8],[9,67.7,72.0,76.2],[10,68.9,73.2,77.5],[11,70.0,74.4,78.8],
        [12,71.0,75.5,80.0],[15,74.1,78.8,83.5],[18,76.9,81.8,86.7],[21,79.4,84.4,89.5],
        [24,81.7,86.9,92.2],[27,83.8,89.2,94.8],[30,85.7,91.3,97.1],[33,87.4,93.2,99.3],
        [36,89.0,95.0,101.4],[42,92.0,98.4,105.4],[48,94.8,101.6,109.1],[54,97.4,104.7,112.7],
        [60,99.9,107.8,116.1]
      ];
    }
    , getWhoHeightGirls: function() {
      return [
        [0,45.4,49.7,54.0],[1,50.0,53.7,57.4],[2,53.2,57.1,61.1],[3,55.8,59.8,63.8],
        [4,58.0,62.1,66.2],[5,59.9,64.0,68.2],[6,61.5,65.7,69.8],[7,62.9,67.1,71.3],
        [8,64.3,68.5,72.7],[9,65.5,69.8,74.0],[10,66.7,71.0,75.2],[11,67.8,72.2,76.5],
        [12,68.9,73.3,77.8],[15,71.9,76.6,81.4],[18,74.6,79.6,84.6],[21,77.1,82.3,87.7],
        [24,79.3,84.7,90.3],[27,81.2,86.9,92.9],[30,83.0,89.0,95.3],[33,84.6,91.0,97.7],
        [36,86.1,92.9,100.1],[42,89.0,96.3,104.0],[48,91.7,99.6,108.0],[54,94.2,102.8,111.9],
        [60,96.7,106.0,115.8]
      ];
    }
    , getWhoHeadBoys: function() {
      // [月龄, P3, P50, P97] 单位: cm
      return [
        [0,32.4,34.5,36.8],[3,38.3,40.5,43.0],[6,40.7,43.0,45.6],[9,42.2,44.5,47.0],
        [12,43.4,45.8,48.3],[18,44.8,47.4,49.9],[24,45.9,48.6,51.3],[36,47.3,50.2,53.1],
        [48,48.3,51.3,54.4],[60,49.0,52.2,55.5]
      ];
    }
    , getWhoHeadGirls: function() {
      return [
        [0,31.9,34.0,36.4],[3,37.3,39.5,41.9],[6,39.6,41.9,44.4],[9,41.0,43.4,45.9],
        [12,42.1,44.6,47.2],[18,43.5,46.1,48.7],[24,44.6,47.3,50.1],[36,46.0,48.9,51.8],
        [48,46.9,50.0,53.1],[60,47.6,50.9,54.1]
      ];
    }
    // 计算体重百分位
    , calcWeightPercentile: function(ageMonth, weightKg, gender) {
      var data = gender==='男' ? this.getWhoWeightBoys() : this.getWhoWeightGirls();
      return this._calcPercentile(ageMonth, weightKg, data);
    }
    // 计算身高百分位
    , calcHeightPercentile: function(ageMonth, heightCm, gender) {
      var data = gender==='男' ? this.getWhoHeightBoys() : this.getWhoHeightGirls();
      return this._calcPercentile(ageMonth, heightCm, data);
    }
    // 内部：返回近似百分位字符串
    , _calcPercentile: function(ageMonth, value, table) {
      // 找最近的两个数据点做线性插值
      var prev = null, next = null;
      for (var i = 0; i < table.length; i++) {
        if (table[i][0] <= ageMonth) prev = table[i];
        if (table[i][0] >= ageMonth && !next) next = table[i];
      }
      if (!prev) prev = table[0];
      if (!next) next = table[table.length-1];
      if (prev[0] === next[0]) {
        var p3=prev[1], p50=prev[3]||prev[2], p97=prev[4]||prev[3];
        if (value < p3) return '<P3'; if (value > p97) return '>P97';
        if (value < (p3+p50)/2) return 'P3-P15';
        if (value < (p50+p97)/2) return 'P50-P85';
        return 'P85-P97';
      }
      var ratio = (ageMonth - prev[0]) / (next[0] - prev[0]);
      var p3v = prev[1] + (next[1]-prev[1])*ratio;
      var p97v = (prev[4]||prev[3]) + ((next[4]||next[3])-(prev[4]||prev[3]))*ratio;
      var p50v = (prev[3]||prev[2]) + ((next[3]||next[2])-(prev[3]||prev[2]))*ratio;
      if (value < p3v) return '<P3(偏低)';
      if (value > p97v) return '>P97(偏高)';
      if (value < p50v*0.97) return 'P3-P15(偏轻)';
      if (value > p50v*1.03) return 'P85-P97(偏重)';
      return 'P15-P85(正常)';
    }
    // 生成生长曲线SVG
    , renderGrowthChart: function(type, gender, records) {
      var isWeight = type === 'weight';
      var isBoy = gender === '男';
      var refData = isWeight
        ? (isBoy ? this.getWhoWeightBoys() : this.getWhoWeightGirls())
        : (isBoy ? this.getWhoHeightBoys() : this.getWhoHeightGirls());
      var unit = type==='weight' ? 'kg' : 'cm';
      var title = type==='weight' ? '体重曲线' : '身高曲线';

      var W=340, H=220, padL=40, padR=15, padT=15, padB=30;
      var refW = W - padL - padR, refH = H - padT - padB;

      // 找数据范围
      var allVals = [];
      refData.forEach(function(d){allVals.push(d[1],d[2],d[3]||d[2]);});
      if (records) records.forEach(function(r){allVals.push(parseFloat(r.value));});
      var minM=0, maxM=36;
      var minV=Math.min.apply(null,allVals)*0.9, maxV=Math.max.apply(null,allVals)*1.1;

      function mX(m){return padL + (m-minM)/(maxM-minM)*refW;}
      function mY(v){return padT + refH - (v-minV)/(maxV-minV)*refH;}

      var svg = '<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;max-width:'+W+'px;background:#FAFAFA;border-radius:12px">';
      // 网格线
      for(var i=0;i<=4;i++){
        var y = padT + refH*i/4;
        svg += '<line x1="'+padL+'" y1="'+y+'" x2="'+(W-padR)+'" y2="'+y+'" stroke="#E5E7EB" stroke-width="1"/>';
      }
      // P3/P97区域
      svg += '<path d="'+refData.map(function(d){return mX(d[0])+','+mY(d[1]);}).join('L')+' '+refData.slice().reverse().map(function(d){return mX(d[0])+','+mY(d[4]||d[3]);}).join('L')+'Z" fill="#FEE2E2" opacity="0.6"/>';
      // P15-P85区域
      svg += '<path d="'+refData.map(function(d){return mX(d[0])+','+mY(d[2]||d[1]);}).join('L')+' '+refData.slice().reverse().map(function(d){return mX(d[0])+','+mY(d[3]||d[2]);}).join('L')+'Z" fill="#D1FAE5" opacity="0.5"/>';
      // P3线
      svg += '<polyline points="'+refData.map(function(d){return mX(d[0])+' '+mY(d[1]);}).join(' ')+'" fill="none" stroke="#FCA5A5" stroke-width="1.5" stroke-dasharray="3,2"/>';
      // P97线
      svg += '<polyline points="'+refData.map(function(d){return mX(d[0])+' '+mY(d[4]||d[3]);}).join(' ')+'" fill="none" stroke="#FCA5A5" stroke-width="1.5" stroke-dasharray="3,2"/>';
      // P50线
      svg += '<polyline points="'+refData.map(function(d){return mX(d[0])+' '+mY(d[3]||d[2]);}).join(' ')+'" fill="none" stroke="#10B981" stroke-width="2"/>';
      // 数据点
      if (records && records.length > 0) {
        svg += '<polyline points="'+records.map(function(r){return mX(r.ageMonth)+' '+mY(parseFloat(r.value));}).join(' ')+'" fill="none" stroke="#FF9B5E" stroke-width="2.5"/>';
        records.forEach(function(r){
          svg += '<circle cx="'+mX(r.ageMonth)+'" cy="'+mY(parseFloat(r.value))+'" r="4" fill="#FF9B5E" stroke="#fff" stroke-width="2"/>';
        });
      }
      // X轴标签
      for(var m=0;m<=36;m+=6){
        svg += '<text x="'+mX(m)+'" y="'+(H-5)+'" text-anchor="middle" font-size="10" fill="#6B7280">'+m+'月</text>';
      }
      svg += '<text x="'+(W/2)+'" y="12" text-anchor="middle" font-size="12" font-weight="600" fill="#374151">'+title+'</text>';
      svg += '</svg>';
      return svg;
    }
  };
})();


// ======== KNOWLEDGE ENGINE v1.0 ========

// ============================================================
// BabyGrow Knowledge Engine v1.0 - Hangzhou MVP
// 一人带娃SOP知识库引擎
// ============================================================

(function() {
  'use strict';

  // ---- Knowledge Base Loader ----
  // Each KB module exports load() -> Promise
  // All data merges into window.KNOWLEDGE namespace

  function loadTextFile(path) {
    return fetch(path)
      .then(function(r) { return r.text(); })
      .catch(function() { return null; });
  }

  function loadYaml文本(path) {
    // Simple YAML parser for our flat-ish structure
    // Real implementation: use js-yaml library
    return loadTextFile(path).then(function(text) {
      if (!text) return {};
      var result = {};
      var currentSection = null;
      var lines = text.split('\n');
      var inBlock = false;
      var blockKey = null;
      var blockLines = [];

      lines.forEach(function(line) {
        // Handle block scalars (| / >)
        if (inBlock) {
          if (line.match(/^\S/)) {
            // Next key, close block
            result[blockKey] = blockLines.join('\n').trim();
            inBlock = false;
            blockLines = [];
          } else {
            blockLines.push(line);
            return;
          }
        }

        if (inBlock) {
          blockLines.push(line);
          return;
        }

        line = line.replace(/^\s*/, '');
        if (!line || line.startsWith('#')) return;

        // Block scalar
        var blockMatch = line.match(/^(\w+):\s*[|>]\s*$/);
        if (blockMatch) {
          inBlock = true;
          blockKey = blockMatch[1];
          return;
        }

        // Key-value
        var kvMatch = line.match(/^(\w+(?:_\w+)*):\s*(.+)$/);
        if (kvMatch) {
          result[kvMatch[1]] = kvMatch[2].trim().replace(/^["']|["']$/g, '');
        }
      });

      if (inBlock && blockKey) {
        result[blockKey] = blockLines.join('\n').trim();
      }

      return result;
    });
  }

  function loadAllKnowledge() {
    var base = '/knowledge/hangzhou/';
    var promises = [
      loadYaml文本(base + 'city_overview.yaml').then(function(d) {
        window.__KB.cityOverview = d;
      }),
      loadYaml文本(base + 'seasonal_ingredients.yaml').then(function(d) {
        window.__KB.seasonalIngredients = d;
      }),
      loadYaml文本(base + 'weather_patterns.yaml').then(function(d) {
        window.__KB.weatherPatterns = d;
      }),
      loadYaml文本(base + 'transit/metro.yaml').then(function(d) {
        window.__KB.transit = d;
      }),
      loadYaml文本(base + 'sop_templates/one_person_care.yaml').then(function(d) {
        window.__KB.sopTemplates = d;
      }),
    ];

    // Load district files
    ['binjiang', 'xihu', 'shangcheng', 'gongshu'].forEach(function(dist) {
      promises.push(loadYaml文本(base + 'districts/' + dist + '.yaml').then(function(d) {
        window.__KB.districts = window.__KB.districts || {};
        window.__KB.districts[dist] = d;
      }));
    });

    return Promise.all(promises);
  }

  // ============================================================
  // Public API: window.KNOWLEDGE.*
  // ============================================================

  window.__KB = {
    ready: false,
    cityOverview: null,
    seasonalIngredients: null,
    weatherPatterns: null,
    transit: null,
    sopTemplates: null,
    districts: {},

    init: function() {
      if (this.ready) return Promise.resolve();
      var self = this;
      return loadAllKnowledge().then(function() {
        self.ready = true;
        console.log('[KB] Knowledge base loaded for Hangzhou');
      });
    },

    // ---- 获取当前季节 ----
    getSeason: function(date) {
      date = date || new Date();
      var m = date.getMonth() + 1;
      if (m >= 3 && m <= 5) return 'spring';
      if (m >= 6 && m <= 8) return 'summer';
      if (m >= 9 && m <= 11) return 'autumn';
      return 'winter';
    },

    // ---- 获取应季食材 ----
    getSeasonalIngredients: function(date, category) {
      var season = this.getSeason(date);
      var si = this.seasonalIngredients;
      if (!si || !si[season]) return [];
      var items = si[season].local_produce || [];
      if (category) {
        items = items.filter(function(i) { return i.category === category; });
      }
      return items;
    },

    // ---- 获取全年通用食材 ----
    getYearRoundIngredients: function(category) {
      var si = this.seasonalIngredients;
      if (!si || !si.year_round) return [];
      var items = [];
      Object.keys(si.year_round).forEach(function(cat) {
        (si.year_round[cat] || []).forEach(function(name) {
          items.push({ name: name, category: cat, year_round: true });
        });
      });
      if (category) {
        items = items.filter(function(i) { return i.category === category; });
      }
      return items;
    },

    // ---- 户外活动推荐（根据天气） ----
    recommendOutdoor: function(weather) {
      // weather: { temp, aqi, rain_mm_h, condition }
      var rules = this.weatherPatterns && this.weatherPatterns.outdoor_activity_rules || [];
      var defaults = this.weatherPatterns && this.weatherPatterns.indoor_backup_required_months || [];

      // Check month-based indoor requirement
      var now = new Date();
      var month = now.getMonth() + 1;
      var needsIndoor = defaults.some(function(m) {
        if (typeof m === 'number') return m === month;
        if (typeof m === 'string' && m.includes(month)) return true;
        return false;
      });
      if (needsIndoor) {
        return { recommendation: 'indoor', reason: '当前月份(' + month + '月)天气不稳定，建议室内活动' };
      }

      var aqi = weather.aqi || 50;
      var temp = weather.temp || 25;
      var rain = weather.rain_mm_h || 0;

      if (aqi > 200) {
        return { recommendation: 'indoor', reason: '空气质量严重污染(AQI=' + aqi + ')' };
      }
      if (aqi > 150) {
        return { recommendation: 'indoor', reason: '空气质量中度污染(AQI=' + aqi + ')，敏感人群建议室内' };
      }
      if (rain >= 10) {
        return { recommendation: 'indoor', reason: '大雨天气，不建议户外' };
      }
      if (rain >= 2.5) {
        return { recommendation: 'indoor', reason: '中雨天气，建议室内' };
      }
      if (temp < 5) {
        return { recommendation: 'indoor', reason: '气温过低(' + temp + '°C)' };
      }
      if (temp > 35) {
        return { recommendation: 'outdoor_morning', reason: '高温天气(' + temp + '°C)，仅早晨傍晚适合户外' };
      }
      if (temp > 32) {
        return { recommendation: 'outdoor_early', reason: '气温较高(' + temp + '°C)，注意防暑' };
      }
      return { recommendation: 'outdoor', reason: '天气适宜，适合户外活动' };
    },

    // ---- 获取区县资源 ----
    getDistrictResources: function(district, type) {
      // district: 'binjiang', 'xihu', etc.
      // type: 'outdoor_parks', 'indoor_playgrounds', 'hospitals', etc.
      var d = this.districts[district];
      if (!d) return [];
      if (type) return d[type] || [];
      return d;
    },

    // ---- 获取区县推荐户外地点（按月龄过滤）----
    getRecommendedParks: function(district, ageMonths) {
      var parks = this.getDistrictResources(district, 'outdoor_parks');
      var minAge = ageMonths >= 12 ? '12m' : '6m';
      return parks.filter(function(p) {
        var sa = p.suitable_age || [];
        // Accept if age range includes minAge or is "全年龄"
        if (sa.indexOf('全年龄') >= 0) return true;
        // Simple check - could be improved
        return true;
      }).map(function(p) {
        return {
          name: p.name,
          type: p.type,
          address: p.address,
          suitable_age: p.suitable_age,
          best_time: p.best_time,
          subway: p.subway_access,
          notes: p.notes,
          travel_time_min: p.travel_time_min || 20
        };
      });
    },

    // ---- 获取SOP模板 ----
    getSOPTemplate: function(templateType) {
      var st = this.sopTemplates;
      if (!st) return null;
      if (templateType) return st[templateType] || null;
      return st;
    },

    // ---- 获取每日框架（工作日/周末）----
    getDailyFramework: function(isWeekend) {
      var st = this.sopTemplates;
      if (!st) return null;
      return isWeekend ? st.daily_framework : st.weekend_framework;
    },

    // ---- 获取活动Prep链 ----
    getActivityPrepChain: function(activityType) {
      var st = this.sopTemplates;
      if (!st || !st.activity_types) return [];
      var at = st.activity_types[activityType];
      if (!at) return [];
      return at.prep_chain || [];
    },

    // ---- 获取活动材料清单 ----
    getActivityMaterials: function(activityType) {
      var st = this.sopTemplates;
      if (!st || !st.activity_types) return [];
      var at = st.activity_types[activityType];
      if (!at) return [];
      return at.materials_needed || [];
    },

    // ---- 特殊场景SOP ----
    getSpecialScenarioSOP: function(scenarioKey) {
      var st = this.sopTemplates;
      if (!st || !st.special_scenarios) return null;
      return st.special_scenarios[scenarioKey] || null;
    },

    // ---- 获取附近亲子地点 ----
    getNearbyPlaces: function(district, placeType, ageMonths) {
      var types = placeType ? [placeType] : [
        'outdoor_parks', 'indoor_playgrounds', 'hospitals', 'libraries'
      ];
      var results = [];
      var self = this;
      types.forEach(function(t) {
        var places = self.getDistrictResources(district, t) || [];
        places.forEach(function(p) {
          results.push({
            name: p.name,
            type: t,
            address: p.address,
            lat_lng: p.lat_lng,
            suitable_age: p.suitable_age,
            best_time: p.best_time,
            subway: p.subway_nearby || p.subway,
            notes: p.notes,
            distance: p.distance || null
          });
        });
      });
      return results;
    },

    // ---- 地铁线路信息 ----
    getMetroInfo: function() {
      return this.transit;
    },

    // ---- 生成完整SOP建议（供AI使用）----
    buildSOPContext: function(childProfile, location, date) {
      var self = this;
      var isWeekend = date && new Date(date).getDay() === 0 || new Date(date).getDay() === 6;
      var framework = this.getDailyFramework(isWeekend);
      var season = this.getSeason(date);

      // Mock weather - in production this comes from weather API
      var weather = {
        temp: 24,
        aqi: 60,
        rain_mm_h: 0,
        condition: '多云'
      };

      var outdoorRec = this.recommendOutdoor(weather);

      var context = {
        version: '1.0',
        city: '杭州',
        district: location.district || '滨江区',
        date: date || new Date().toISOString().split('T')[0],
        isWeekend: isWeekend,
        season: season,
        framework: framework,
        weather: weather,
        outdoorRecommendation: outdoorRec,
        seasonalIngredients: this.getSeasonalIngredients(date),
        yearRoundIngredients: this.getYearRoundIngredients(),
        district: location.district,
        nearbyPlaces: this.getNearbyPlaces(location.district, null, childProfile.age_months),
        metro: this.getMetroInfo(),
        activityTemplates: this.getSOPTemplate('activity_types'),
        specialScenarios: this.getSOPTemplate('special_scenarios')
      };
      return context;
    }
  };

  // Expose as KNOWLEDGE (alias)
  window.KNOWLEDGE = window.__KB;

  // Auto-init after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      window.__KB.init();
    });
  } else {
    window.__KB.init();
  }

})();




// ======== KNOWLEDGE ENGINE v2.0 - Hangzhou SOP (JSON) ========
(function() {
  'use strict';

  var BASE = '/web/knowledge/hangzhou/';

  var FILE_MAP = {
    'city_overview': BASE + 'city_overview.json',
    'seasonal_ingredients': BASE + 'seasonal_ingredients.json',
    'weather_patterns': BASE + 'weather_patterns.json',
    'sop_templates': BASE + 'sop_templates/one_person_care.json',
    'transit_metro': BASE + 'transit/metro.json',
    'district_binjiang': BASE + 'districts/binjiang.json',
    'district_xihu': BASE + 'districts/xihu.json',
    'district_shangcheng': BASE + 'districts/shangcheng.json',
    'district_gongshu': BASE + 'districts/gongshu.json',
    'city_meta': BASE + 'city_meta.json'
  };

  function loadJSON(url) {
    return fetch(url)
      .then(function(r) { return r.json(); })
      .catch(function() { return null; });
  }

  function loadAll() {
    var keys = Object.keys(FILE_MAP);
    var promises = keys.map(function(k) {
      return loadJSON(FILE_MAP[k]).then(function(data) {
        KB.data[k] = data;
      });
    });
    return Promise.all(promises);
  }

  var KB = {
    ready: false,
    data: {},

    init: function() {
      var self = this;
      return loadAll().then(function() {
        self.ready = true;
        console.log('[KB] Hangzhou SOP v2.0 loaded');
      });
    },

    _d: function(key) { return this.data[key] || null; },

    getSeason: function(date) {
      var d = date;
      if (typeof d === 'string') d = new Date(d);
      if (!d || isNaN(d.getTime())) d = new Date();
      var m = d.getMonth() + 1;
      if (m >= 3 && m <= 5) return 'spring';
      if (m >= 6 && m <= 8) return 'summer';
      if (m >= 9 && m <= 11) return 'autumn';
      return 'winter';
    },

    getSeasonalIngredients: function(date, category) {
      var d = this._d('seasonal_ingredients');
      if (!d) return [];
      var season = this.getSeason(date);
      var list = d[season] && d[season].local_produce || [];
      if (category) list = list.filter(function(i) { return i.category === category; });
      return list;
    },

    getYearRoundIngredients: function(category) {
      var d = this._d('seasonal_ingredients');
      if (!d) return [];
      var result = [];
      var yr = d.year_round || {};
      Object.keys(yr).forEach(function(cat) {
        (yr[cat] || []).forEach(function(name) {
          result.push({ name: name, category: cat, year_round: true });
        });
      });
      if (category) result = result.filter(function(i) { return i.category === category; });
      return result;
    },

    recommendOutdoor: function(w) {
      var d = this._d('weather_patterns');
      var defaults = d && d.indoor_backup_required_months || [];
      var now = new Date();
      var month = now.getMonth() + 1;
      if (defaults.indexOf(month) >= 0) {
        return { recommendation: 'indoor', reason: month + '月天气不稳定，建议室内' };
      }
      var aqi = w.aqi || 50, temp = w.temp || 25, rain = w.rain_mm_h || 0;
      if (aqi > 200) return { recommendation: 'indoor', reason: 'AQI严重污染(' + aqi + ')' };
      if (aqi > 150) return { recommendation: 'indoor', reason: 'AQI中度污染(' + aqi + ')' };
      if (rain >= 10) return { recommendation: 'indoor', reason: '大雨天气' };
      if (rain >= 2.5) return { recommendation: 'indoor', reason: '中雨天气' };
      if (temp < 5) return { recommendation: 'indoor', reason: '气温过低' };
      if (temp > 35) return { recommendation: 'outdoor_morning', reason: '高温' };
      if (temp > 32) return { recommendation: 'outdoor_early', reason: '气温较高，注意防暑' };
      return { recommendation: 'outdoor', reason: '天气适宜' };
    },

    // ---- District resources ----
    getDistrict: function(name) {
      return this._d('district_' + name);
    },
    getDistrictParks: function(district) {
      var d = this.getDistrict(district);
      return d && d.outdoor_parks || [];
    },
    getDistrictHospitals: function(district) {
      var d = this.getDistrict(district);
      return d && d.hospitals || [];
    },
    getDistrictIndoor: function(district) {
      var d = this.getDistrict(district);
      return d && d.indoor_playgrounds || [];
    },
    getDistrictLibraries: function(district) {
      var d = this.getDistrict(district);
      return d && d.libraries || [];
    },
    getDistrictMarkets: function(district) {
      var d = this.getDistrict(district);
      return d && d.wet_market && [d.wet_market] || [];
    },
    getDistrictDelivery: function(district) {
      var d = this.getDistrict(district);
      return d && d.delivery_services || [];
    },

    // ---- SOP Templates ----
    getDailyFramework: function(isWeekend) {
      var d = this._d('sop_templates');
      if (!d) return null;
      return isWeekend ? d.weekend_framework : d.daily_framework;
    },
    getActivityPrepChain: function(type) {
      var d = this._d('sop_templates');
      var at = d && d.activity_types && d.activity_types[type];
      return at && at.prep_chain || [];
    },
    getActivityMaterials: function(type) {
      var d = this._d('sop_templates');
      var at = d && d.activity_types && d.activity_types[type];
      return at && at.materials_needed || [];
    },
    getSpecialScenario: function(key) {
      var d = this._d('sop_templates');
      return d && d.special_scenarios && d.special_scenarios[key] || null;
    },

    // ---- City-level ----
    getCityOverview: function() { return this._d('city_overview'); },
    getWeatherPatterns: function() { return this._d('weather_patterns'); },
    getMetro: function() { return this._d('transit_metro'); },

    // ---- Comprehensive SOP context for AI ----
    buildSOPContext: function(child, location, date) {
      var isWeekend = false;
      var d = date;
      if (typeof d === 'string') d = new Date(d);
      if (d && !isNaN(d.getTime())) {
        var day = d.getDay();
        isWeekend = day === 0 || day === 6;
      }
      var district = location && location.district || 'binjiang';
      var season = this.getSeason(date);
      return {
        version: '2.0',
        city: '杭州',
        district: district,
        date: date || new Date().toISOString().split('T')[0],
        isWeekend: isWeekend,
        season: season,
        child: {
          age_months: child && child.months || child && child.age_months,
          gender: child && child.gender
        },
        framework: this.getDailyFramework(isWeekend),
        weather: { temp: 24, aqi: 60, rain_mm_h: 0, condition: '多云' },
        outdoorRecommendation: this.recommendOutdoor({ temp: 24, aqi: 60, rain_mm_h: 0 }),
        seasonalIngredients: this.getSeasonalIngredients(date),
        yearRoundIngredients: this.getYearRoundIngredients(),
        districtOverview: this.getDistrict(district),
        nearbyParks: this.getDistrictParks(district),
        nearbyHospitals: this.getDistrictHospitals(district),
        nearbyIndoor: this.getDistrictIndoor(district),
        nearbyLibraries: this.getDistrictLibraries(district),
        nearbyMarkets: this.getDistrictMarkets(district),
        deliveryServices: this.getDistrictDelivery(district),
        metro: this.getMetro(),
        activityTemplates: (this._d('sop_templates') || {}).activity_types,
        specialScenarios: (this._d('sop_templates') || {}).special_scenarios,
        cityOverview: this.getCityOverview(),
        cityWeatherPatterns: this.getWeatherPatterns()
      };
    }
  };

  window.KNOWLEDGE = window.__KB = KB;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { KB.init(); });
  } else {
    KB.init();
  }

})();
