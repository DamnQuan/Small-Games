import pygame
import sys
import os

# 初始化pygame
pygame.init()

# 设置中文字体
pygame.font.init()
print("系统可用字体列表:", pygame.font.get_fonts())

# 尝试加载中文字体
game_font = None

# 方法1: 尝试使用pygame.font.Font直接加载系统TTF文件
# 常见中文字体路径
common_font_paths = [
    '/System/Library/Fonts/PingFang.ttc',    # macOS 苹方
    '/Library/Fonts/SimHei.ttf',            # macOS 黑体
    '/Library/Fonts/Microsoft YaHei.ttf',   # Windows 雅黑
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux 文泉驿
    '/usr/share/fonts/truetype/simhei/simhei.ttf'      # Linux 黑体
]

print("尝试直接加载TTF文件...")
for font_path in common_font_paths:
    if os.path.exists(font_path):
        try:
            game_font = pygame.font.Font(font_path, 36)
            print(f"成功直接加载字体文件: {font_path}")
            break
        except Exception as e:
            print(f"加载TTF文件失败 {font_path}: {e}")

# 方法2: 如果TTF文件加载失败，尝试使用SysFont
if not game_font:
    print("尝试使用SysFont加载系统字体...")
    # 中文字体选项列表，按优先级排序
    font_options = [
        ('simhei', '黑体'),
        ('wenquanyi', '文泉驿'),
        ('heiti', '黑体'),
        ('pingfang', '苹方'),
        ('microsoftyahei', '微软雅黑'),
        ('msyh', '微软雅黑'),
        ('notosanssc', '思源黑体'),
        ('noto', 'Noto'),
        ('arialunicode', 'Arial Unicode'),
        ('simsun', '宋体')
    ]
    
    available_fonts = [font.lower() for font in pygame.font.get_fonts()]
    print("可用字体:", available_fonts)
    
    for font_base, font_desc in font_options:
        for available_font in available_fonts:
            if font_base in available_font:
                try:
                    game_font = pygame.font.SysFont(available_font, 36)
                    print(f"成功加载系统字体: {available_font} ({font_desc})")
                    # 测试中文字体渲染
                    test_surface = game_font.render("测试中文显示", True, (255, 255, 255))
                    print(f"字体测试成功，渲染高度: {test_surface.get_height()}")
                    break
                except Exception as e:
                    print(f"加载字体失败 {available_font}: {e}")
        if game_font:
            break

# 方法3: 如果以上都失败，使用默认字体但做更多调试
if not game_font:
    try:
        game_font = pygame.font.SysFont(None, 36)
        print("使用默认字体，尝试最大兼容性模式")
        # 尝试用默认字体渲染
        test_surface = game_font.render("? 中文可能无法显示 ?", True, (255, 255, 255))
        print(f"默认字体测试，渲染高度: {test_surface.get_height()}")
    except:
        print("警告: 无法加载任何字体，游戏可能无法正常显示文字")

# 添加全局字体对象以便所有游戏类使用
def get_font(size=None):
    """获取指定大小的字体"""
    if size and game_font:
        # 尝试创建新字体实例
        try:
            if hasattr(game_font, 'name'):
                return pygame.font.SysFont(game_font.name, size)
            elif hasattr(game_font, 'get_height'):  # 如果是Font对象
                # 对于直接加载的TTF文件，尝试创建相同字体但不同大小
                try:
                    font_path = game_font.path
                    return pygame.font.Font(font_path, size)
                except:
                    # 如果失败，返回原始字体
                    return game_font
            else:
                return game_font
        except Exception as e:
            print(f"创建特定大小字体失败: {e}")
            return game_font
    return game_font

def render_text(text, color, size=None):
    """安全地渲染文本，处理可能的中文显示问题"""
    try:
        font = get_font(size)
        return font.render(text, True, color)
    except Exception as e:
        print(f"渲染文本失败 '{text}': {e}")
        # 尝试用英文替代或使用默认字体
        try:
            fallback_font = pygame.font.SysFont(None, size or 36)
            return fallback_font.render("?" * len(text), True, color)
        except:
            # 如果所有都失败，返回一个空的surface
            return pygame.Surface((len(text) * 10, 36))

# 游戏常量 - 提高分辨率以便更好地显示所有游戏
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('多合一游戏集合')
clock = pygame.time.Clock()

# 游戏管理类
class GameManager:
    def __init__(self):
        self.current_game = None
        self.game_list = [
            "贪吃蛇",
            "打砖块",
            "乒乓球",
            "俄罗斯方块",
            "井字棋",
            "数字拼图",
            "2048",
            "猜数字"
        ]
        self.menu_selected = 0
        self.state = "menu"  # menu, game, gameover
    
    def run_menu(self):
        screen.fill(BLACK)
        
        # 创建背景渐变色效果
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            r = int(0 + (30 - 0) * y / SCREEN_HEIGHT)
            g = int(0 + (30 - 0) * y / SCREEN_HEIGHT)
            b = int(0 + (60 - 0) * y / SCREEN_HEIGHT)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        screen.blit(background, (0, 0))
        
        # 绘制标题 - 使用安全的文本渲染函数，调整字体大小
        title = render_text("多合一游戏集合", WHITE, 56)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 120))
        # 添加标题阴影
        shadow_title = render_text("多合一游戏集合", (50, 50, 50), 56)
        screen.blit(shadow_title, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)
        
        # 绘制游戏列表，增加间距避免堆叠
        menu_start_y = 200
        menu_spacing = 60  # 增加间距
        
        for i, game_name in enumerate(self.game_list):
            color = YELLOW if i == self.menu_selected else WHITE
            text = render_text(game_name, color, 32)  # 稍小的字体避免文字堆叠
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, menu_start_y + i * menu_spacing))
            
            # 如果是选中项，添加高亮背景
            if i == self.menu_selected:
                highlight_rect = pygame.Rect(0, 0, text_rect.width + 40, text_rect.height + 15)
                highlight_rect.center = text_rect.center
                pygame.draw.rect(screen, (100, 100, 100), highlight_rect, 0, 10)
            
            screen.blit(text, text_rect)
        
        # 绘制提示
        hint = render_text("上下箭头选择，回车确认，ESC返回", WHITE, 24)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 80))
        screen.blit(hint, hint_rect)
        
        # 显示版本信息
        version_info = render_text("v1.0.0", (100, 100, 100), 16)
        screen.blit(version_info, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))
    
    def run_game(self):
        if self.current_game:
            self.current_game.run()
    
    def handle_events(self):
        # 获取所有事件
        events = pygame.event.get()
        
        # 处理每个事件
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            # 菜单状态处理
            if self.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(self.game_list)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(self.game_list)
                    elif event.key == pygame.K_RETURN:
                        self.start_game(self.menu_selected)
                        self.state = "game"
            
            # 游戏状态处理
            elif self.state == "game" and self.current_game:
                # 处理返回菜单的通用按键
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_game = None
                    self.state = "menu"
                # 将事件传递给当前游戏的handle_event方法（如果有）
                if hasattr(self.current_game, 'handle_event'):
                    self.current_game.handle_event(event)
        
        return True
    
    def start_game(self, game_index):
        game_name = self.game_list[game_index]
        
        if game_name == "贪吃蛇":
            self.current_game = SnakeGame()
        elif game_name == "打砖块":
            self.current_game = BreakoutGame()
        elif game_name == "乒乓球":
            self.current_game = PongGame()
        elif game_name == "俄罗斯方块":
            self.current_game = TetrisGame()
        elif game_name == "井字棋":
            self.current_game = TicTacToeGame()
        elif game_name == "数字拼图":
            self.current_game = PuzzleGame()
        elif game_name == "2048":
            self.current_game = Game2048()
        elif game_name == "猜数字":
            self.current_game = GuessNumberGame()

# 贪吃蛇游戏类
class SnakeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_dir = "RIGHT"
        self.next_dir = "RIGHT"
        self.food = (300, 300)
        self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        import random
        self.food = (random.randint(1, (SCREEN_WIDTH-20)//10) * 10, 
                    random.randint(1, (SCREEN_HEIGHT-20)//10) * 10)
        if self.food in self.snake:
            self.generate_food()
    
    def handle_event(self, event):
        """处理单个事件，由GameManager传递"""
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                # 游戏结束状态下的按键处理
                if event.key == pygame.K_r:
                    self.reset()
            else:
                # 游戏进行中的按键处理
                if event.key == pygame.K_UP and self.snake_dir != "DOWN":
                    self.next_dir = "UP"
                elif event.key == pygame.K_DOWN and self.snake_dir != "UP":
                    self.next_dir = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake_dir != "RIGHT":
                    self.next_dir = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake_dir != "LEFT":
                    self.next_dir = "RIGHT"
    
    def run(self):
        if not self.game_over:
            # 更新方向
            self.snake_dir = self.next_dir
            
            # 移动蛇
            head_x, head_y = self.snake[0]
            if self.snake_dir == "UP":
                head_y -= 10
            elif self.snake_dir == "DOWN":
                head_y += 10
            elif self.snake_dir == "LEFT":
                head_x -= 10
            elif self.snake_dir == "RIGHT":
                head_x += 10
            
            # 检查边界碰撞
            if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
                self.game_over = True
            
            # 检查自身碰撞
            if (head_x, head_y) in self.snake[1:]:
                self.game_over = True
            
            # 更新蛇身
            self.snake.insert(0, (head_x, head_y))
            
            # 检查食物
            if (head_x, head_y) == self.food:
                self.score += 10
                self.generate_food()
            else:
                self.snake.pop()
        
        # 绘制游戏
        if self.game_over:
            self.show_game_over()
        else:
            self.draw()
    
    def draw(self):
        # 创建渐变背景
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            r = int(10 + (30 - 10) * y / SCREEN_HEIGHT)
            g = int(30 + (50 - 30) * y / SCREEN_HEIGHT)
            b = int(10 + (20 - 10) * y / SCREEN_HEIGHT)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        screen.blit(background, (0, 0))
        
        # 绘制游戏区域边框
        game_area = pygame.Rect(5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 90)
        pygame.draw.rect(screen, (50, 100, 50), game_area, 2)
        
        # 绘制蛇身
        for segment in self.snake[1:]:
            pygame.draw.rect(screen, (30, 200, 30), (segment[0], segment[1], 10, 10), 0, 2)
        
        # 绘制头部（带眼睛效果）
        pygame.draw.rect(screen, (255, 215, 0), (self.snake[0][0], self.snake[0][1], 10, 10), 0, 2)
        # 眼睛
        eye_size = 2
        if self.snake_dir == "RIGHT":
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 7, self.snake[0][1] + 3), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 7, self.snake[0][1] + 7), eye_size)
        elif self.snake_dir == "LEFT":
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 3, self.snake[0][1] + 3), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 3, self.snake[0][1] + 7), eye_size)
        elif self.snake_dir == "UP":
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 3, self.snake[0][1] + 3), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 7, self.snake[0][1] + 3), eye_size)
        elif self.snake_dir == "DOWN":
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 3, self.snake[0][1] + 7), eye_size)
            pygame.draw.circle(screen, (0, 0, 0), (self.snake[0][0] + 7, self.snake[0][1] + 7), eye_size)
        
        # 绘制食物（苹果样式）
        pygame.draw.rect(screen, (255, 0, 0), (self.food[0], self.food[1], 10, 10), 0, 5)
        # 食物顶部叶子
        pygame.draw.polygon(screen, (0, 255, 0), [(self.food[0]+5, self.food[1]), 
                                                (self.food[0]+8, self.food[1]-3), 
                                                (self.food[0]+2, self.food[1]-3)])
        
        # 绘制信息栏
        info_bar = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, (50, 50, 50), info_bar, 0)
        pygame.draw.rect(screen, (80, 80, 80), info_bar, 1)
        
        # 绘制分数和控制提示
        score_text = render_text(f"分数: {self.score}", YELLOW, 32)
        screen.blit(score_text, (20, SCREEN_HEIGHT - 60))
        
        controls_text = render_text("方向键控制蛇的移动", WHITE, 24)
        screen.blit(controls_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 60))
    
    def show_game_over(self):
        # 创建半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # 创建游戏结束面板
        game_over_panel = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 150, 400, 300)
        pygame.draw.rect(screen, (80, 30, 30), game_over_panel, 0, 10)
        pygame.draw.rect(screen, (150, 50, 50), game_over_panel, 2, 10)
        
        # 绘制游戏结束文本
        game_over_text = render_text("游戏结束！", RED, 48)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
        screen.blit(game_over_text, game_over_rect)
        
        # 绘制最终分数
        final_score = render_text(f"最终分数: {self.score}", YELLOW, 36)
        final_score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
        screen.blit(final_score, final_score_rect)
        
        # 绘制重新开始提示
        restart_text = render_text("按R重新开始，按ESC返回", WHITE, 28)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        screen.blit(restart_text, restart_rect)

# 打砖块游戏类
class BreakoutGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_x = SCREEN_WIDTH // 2 - self.paddle_width // 2
        self.paddle_y = SCREEN_HEIGHT - 50
        self.paddle_speed = 10
        
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_radius = 10
        self.ball_dx = 4
        self.ball_dy = -4
        
        # 创建砖块
        self.bricks = []
        brick_rows = 5
        brick_cols = 10
        brick_width = (SCREEN_WIDTH - 20) // brick_cols
        brick_height = 20
        
        for row in range(brick_rows):
            for col in range(brick_cols):
                brick_x = 10 + col * brick_width
                brick_y = 50 + row * (brick_height + 10)
                brick_color = (255 - row * 30, 50 + row * 40, 100)
                self.bricks.append({
                    'rect': pygame.Rect(brick_x, brick_y, brick_width - 5, brick_height),
                    'color': brick_color
                })
        
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.victory = False
    
    def run(self):
        if self.game_over or self.victory:
            self.show_end_screen()
            return
        
        # 移动挡板
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle_x > 0:
            self.paddle_x -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle_x < SCREEN_WIDTH - self.paddle_width:
            self.paddle_x += self.paddle_speed
        
        # 移动球
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # 墙壁碰撞检测
        if self.ball_x - self.ball_radius <= 0 or self.ball_x + self.ball_radius >= SCREEN_WIDTH:
            self.ball_dx = -self.ball_dx
        if self.ball_y - self.ball_radius <= 0:
            self.ball_dy = -self.ball_dy
        
        # 检测球是否落下
        if self.ball_y - self.ball_radius > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.reset_ball()
        
        # 挡板碰撞检测
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height)
        ball_rect = pygame.Rect(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius, 
                              self.ball_radius * 2, self.ball_radius * 2)
        
        if paddle_rect.colliderect(ball_rect):
            self.ball_dy = -abs(self.ball_dy)
            # 根据击中挡板的位置调整反弹角度
            hit_pos = (self.ball_x - self.paddle_x) / self.paddle_width
            self.ball_dx = (hit_pos - 0.5) * 10
        
        # 砖块碰撞检测
        for brick in self.bricks[:]:
            if ball_rect.colliderect(brick['rect']):
                self.bricks.remove(brick)
                self.score += 10
                self.ball_dy = -self.ball_dy
                break
        
        # 检查胜利条件
        if not self.bricks:
            self.victory = True
        
        # 绘制游戏
        self.draw()
    
    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 4
        self.ball_dy = -4
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制挡板
        pygame.draw.rect(screen, BLUE, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
        
        # 绘制球
        pygame.draw.circle(screen, WHITE, (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        
        # 绘制砖块
        for brick in self.bricks:
            pygame.draw.rect(screen, brick['color'], brick['rect'])
        
        # 绘制分数和生命值
        score_text = game_font.render(f"分数: {self.score}", True, WHITE)
        lives_text = game_font.render(f"生命: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    
    def show_end_screen(self):
        screen.fill(BLACK)
        if self.victory:
            end_text = game_font.render("恭喜你赢了！", True, GREEN)
        else:
            end_text = game_font.render("游戏结束！", True, RED)
        
        score_text = game_font.render(f"最终分数: {self.score}", True, WHITE)
        retry_text = game_font.render("按R重试，按ESC返回", True, WHITE)
        
        screen.blit(end_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return

# 乒乓球游戏类
class PongGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # 玩家球拍
        self.player_width = 15
        self.player_height = 100
        self.player_x = 50
        self.player_y = SCREEN_HEIGHT // 2 - self.player_height // 2
        self.player_speed = 8
        
        # AI球拍
        self.ai_width = 15
        self.ai_height = 100
        self.ai_x = SCREEN_WIDTH - 50 - self.ai_width
        self.ai_y = SCREEN_HEIGHT // 2 - self.ai_height // 2
        self.ai_speed = 5
        
        # 球
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_radius = 10
        self.ball_dx = 5
        self.ball_dy = 5
        
        # 分数
        self.player_score = 0
        self.ai_score = 0
        self.max_score = 10
        self.game_over = False
    
    def run(self):
        if self.game_over:
            self.show_game_over()
            return
        
        # 移动玩家球拍
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_y > 0:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player_y < SCREEN_HEIGHT - self.player_height:
            self.player_y += self.player_speed
        
        # AI移动
        self.ai_move()
        
        # 移动球
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # 墙壁碰撞
        if self.ball_y - self.ball_radius <= 0 or self.ball_y + self.ball_radius >= SCREEN_HEIGHT:
            self.ball_dy = -self.ball_dy
        
        # 检查得分
        if self.ball_x - self.ball_radius <= 0:
            self.ai_score += 1
            if self.ai_score >= self.max_score:
                self.game_over = True
            else:
                self.reset_ball()
        elif self.ball_x + self.ball_radius >= SCREEN_WIDTH:
            self.player_score += 1
            if self.player_score >= self.max_score:
                self.game_over = True
            else:
                self.reset_ball()
        
        # 球拍碰撞
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        ai_rect = pygame.Rect(self.ai_x, self.ai_y, self.ai_width, self.ai_height)
        ball_rect = pygame.Rect(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius, 
                              self.ball_radius * 2, self.ball_radius * 2)
        
        if player_rect.colliderect(ball_rect):
            self.ball_dx = abs(self.ball_dx)
            # 根据击中位置调整角度
            hit_pos = (self.ball_y - self.player_y) / self.player_height
            self.ball_dy = (hit_pos - 0.5) * 10
        elif ai_rect.colliderect(ball_rect):
            self.ball_dx = -abs(self.ball_dx)
            # 根据击中位置调整角度
            hit_pos = (self.ball_y - self.ai_y) / self.ai_height
            self.ball_dy = (hit_pos - 0.5) * 10
        
        # 绘制游戏
        self.draw()
    
    def ai_move(self):
        # 简单的AI逻辑
        if self.ai_y + self.ai_height // 2 < self.ball_y - 20:
            self.ai_y += self.ai_speed
        elif self.ai_y + self.ai_height // 2 > self.ball_y + 20:
            self.ai_y -= self.ai_speed
        
        # 限制AI在屏幕内
        self.ai_y = max(0, min(self.ai_y, SCREEN_HEIGHT - self.ai_height))
    
    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        # 随机方向
        import random
        self.ball_dx = 5 if random.random() > 0.5 else -5
        self.ball_dy = (random.random() - 0.5) * 10
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制中线
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
        
        # 绘制球拍
        pygame.draw.rect(screen, WHITE, (self.player_x, self.player_y, self.player_width, self.player_height))
        pygame.draw.rect(screen, WHITE, (self.ai_x, self.ai_y, self.ai_width, self.ai_height))
        
        # 绘制球
        pygame.draw.circle(screen, WHITE, (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        
        # 绘制分数
        player_text = game_font.render(str(self.player_score), True, WHITE)
        ai_text = game_font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (SCREEN_WIDTH//4, 50))
        screen.blit(ai_text, (SCREEN_WIDTH*3//4, 50))
    
    def show_game_over(self):
        screen.fill(BLACK)
        if self.player_score >= self.max_score:
            result_text = game_font.render("你赢了！", True, GREEN)
        else:
            result_text = game_font.render("电脑赢了！", True, RED)
        
        score_text = game_font.render(f"分数: {self.player_score} - {self.ai_score}", True, WHITE)
        retry_text = game_font.render("按R重试，按ESC返回", True, WHITE)
        
        screen.blit(result_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return

# 俄罗斯方块游戏类（简化版）
class TetrisGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board_width = 10
        self.board_height = 20
        self.cell_size = 30
        
        # 计算游戏区域位置（居中）
        self.board_x = (SCREEN_WIDTH - self.board_width * self.cell_size) // 2
        self.board_y = 50
        
        # 创建空白棋盘
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        
        # 定义方块形状
        self.shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 0], [0, 1, 1]]   # Z
        ]
        
        # 定义额外的颜色
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.ORANGE = (255, 165, 0)
        
        # 方块颜色
        self.colors = [WHITE, RED, GREEN, BLUE, self.CYAN, self.MAGENTA, YELLOW, self.ORANGE]
        
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 1.0  # 每秒下落一次
        self.last_fall_time = pygame.time.get_ticks()
    
    def new_piece(self):
        import random
        shape_idx = random.randint(0, len(self.shapes) - 1)
        shape = self.shapes[shape_idx]
        color_idx = shape_idx + 1  # 0 是空白颜色
        
        # 初始位置
        x = self.board_width // 2 - len(shape[0]) // 2
        y = 0
        
        return {
            'shape': shape,
            'color': color_idx,
            'x': x,
            'y': y
        }
    
    def run(self):
        if self.game_over:
            self.show_game_over()
            return
        
        # 处理输入
        self.handle_input()
        
        # 自动下落
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > (1000 / self.fall_speed):
            if not self.move(0, 1):
                self.lock_piece()
                self.clear_lines()
                self.spawn_new_piece()
            self.last_fall_time = current_time
        
        # 绘制游戏
        self.draw()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if keys[pygame.K_DOWN]:
            if self.move(0, 1):
                self.score += 1
        if keys[pygame.K_UP]:
            self.rotate()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 硬降
                    while self.move(0, 1):
                        self.score += 2
                elif event.key == pygame.K_ESCAPE:
                    return
    
    def move(self, dx, dy):
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
        
        if self.check_collision():
            self.current_piece['x'] -= dx
            self.current_piece['y'] -= dy
            return False
        
        return True
    
    def rotate(self):
        # 旋转形状
        shape = self.current_piece['shape']
        rows, cols = len(shape), len(shape[0])
        rotated = [[shape[rows-j-1][i] for j in range(rows)] for i in range(cols)]
        
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        if self.check_collision():
            # 如果旋转后碰撞，恢复原形状
            self.current_piece['shape'] = old_shape
    
    def check_collision(self):
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 0:
                    continue
                
                # 检查边界
                if (x + j < 0 or x + j >= self.board_width or
                    y + i >= self.board_height):
                    return True
                
                # 检查与已有方块的碰撞
                if y + i >= 0 and self.board[y + i][x + j] != 0:
                    return True
        
        return False
    
    def lock_piece(self):
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        color = self.current_piece['color']
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 0:
                    continue
                
                if y + i >= 0:
                    self.board[y + i][x + j] = color
    
    def clear_lines(self):
        lines_cleared = 0
        i = self.board_height - 1
        
        while i >= 0:
            if all(cell != 0 for cell in self.board[i]):
                # 移除当前行
                del self.board[i]
                # 在顶部添加新行
                self.board.insert(0, [0 for _ in range(self.board_width)])
                lines_cleared += 1
            else:
                i -= 1
        
        # 计算得分
        if lines_cleared > 0:
            self.score += lines_cleared * lines_cleared * 100
            # 更新等级
            self.level = self.score // 1000 + 1
            self.fall_speed = 1.0 + (self.level - 1) * 0.2
    
    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # 检查游戏是否结束
        if self.check_collision():
            self.game_over = True
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制边界
        pygame.draw.rect(screen, WHITE, 
                        (self.board_x - 2, self.board_y - 2, 
                        self.board_width * self.cell_size + 4, 
                        self.board_height * self.cell_size + 4), 2)
        
        # 绘制棋盘
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] != 0:
                    color = self.colors[self.board[i][j]]
                    pygame.draw.rect(screen, color, 
                                    (self.board_x + j * self.cell_size, 
                                    self.board_y + i * self.cell_size, 
                                    self.cell_size - 1, self.cell_size - 1))
        
        # 绘制当前方块
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        color = self.colors[self.current_piece['color']]
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0 and y + i >= 0:
                    pygame.draw.rect(screen, color, 
                                    (self.board_x + (x + j) * self.cell_size, 
                                    self.board_y + (y + i) * self.cell_size, 
                                    self.cell_size - 1, self.cell_size - 1))
        
        # 绘制分数和等级
        score_text = game_font.render(f"分数: {self.score}", True, WHITE)
        level_text = game_font.render(f"等级: {self.level}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))
        
        # 绘制下一个方块预览
        next_text = game_font.render("下一个:", True, WHITE)
        screen.blit(next_text, (SCREEN_WIDTH - 150, 20))
        
        next_shape = self.next_piece['shape']
        next_color = self.colors[self.next_piece['color']]
        
        # 居中绘制下一个方块预览
        preview_x = SCREEN_WIDTH - 150
        preview_y = 60
        shape_width = len(next_shape[0]) * self.cell_size
        shape_height = len(next_shape) * self.cell_size
        
        for i in range(len(next_shape)):
            for j in range(len(next_shape[i])):
                if next_shape[i][j] != 0:
                    pygame.draw.rect(screen, next_color, 
                                    (preview_x + (j * self.cell_size), 
                                    preview_y + (i * self.cell_size), 
                                    self.cell_size - 1, self.cell_size - 1))
    
    def show_game_over(self):
        screen.fill(BLACK)
        game_over_text = game_font.render("游戏结束！", True, RED)
        score_text = game_font.render(f"最终分数: {self.score}", True, WHITE)
        level_text = game_font.render(f"达到等级: {self.level}", True, WHITE)
        retry_text = game_font.render("按R重试，按ESC返回", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 80))
        screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30))
        screen.blit(level_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 80))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return

# 井字棋游戏类
class TicTacToeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]  # 0: 空, 1: X, 2: O
        self.current_player = 1  # 1: 玩家, 2: AI
        self.game_over = False
        self.winner = 0
        self.cell_size = 150
        self.board_start_x = (SCREEN_WIDTH - self.cell_size * 3) // 2
        self.board_start_y = (SCREEN_HEIGHT - self.cell_size * 3) // 2
    
    def handle_event(self, event):
        """处理单个事件，由GameManager传递"""
        if self.game_over:
            # 游戏结束状态下的按键处理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
        else:
            # 游戏进行中的事件处理
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.current_player == 1:
                    x, y = pygame.mouse.get_pos()
                    col = (x - self.board_start_x) // self.cell_size
                    row = (y - self.board_start_y) // self.cell_size
                    
                    if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == 0:
                        self.board[row][col] = 1
                        self.current_player = 2
    
    def run(self):
        # 如果游戏未结束且轮到AI回合
        if not self.game_over and self.current_player == 2:
            self.ai_move()
            self.check_game_state()
        
        # 绘制游戏
        if self.game_over:
            self.show_game_over()
        else:
            self.draw()
    
    def ai_move(self):
        # 简单的AI逻辑：优先赢，然后阻止玩家赢，否则随机选择
        # 检查是否有获胜机会
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 2
                    if self.check_winner(2):
                        return
                    self.board[i][j] = 0
        
        # 检查是否需要阻止玩家获胜
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 1
                    if self.check_winner(1):
                        self.board[i][j] = 2
                        return
                    self.board[i][j] = 0
        
        # 选择第一个可用位置
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 2
                    self.current_player = 1
                    return
    
    def check_game_state(self):
        # 检查玩家胜利
        if self.check_winner(1):
            self.winner = 1
            self.game_over = True
        # 检查AI胜利
        elif self.check_winner(2):
            self.winner = 2
            self.game_over = True
        # 检查平局
        elif all(self.board[i][j] != 0 for i in range(3) for j in range(3)):
            self.winner = 0
            self.game_over = True
    
    def check_winner(self, player):
        # 检查行
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        # 检查列
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        # 检查对角线
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制棋盘
        for i in range(1, 3):
            # 横线
            pygame.draw.line(screen, WHITE, 
                            (self.board_start_x, self.board_start_y + i * self.cell_size),
                            (self.board_start_x + 3 * self.cell_size, self.board_start_y + i * self.cell_size),
                            3)
            # 竖线
            pygame.draw.line(screen, WHITE, 
                            (self.board_start_x + i * self.cell_size, self.board_start_y),
                            (self.board_start_x + i * self.cell_size, self.board_start_y + 3 * self.cell_size),
                            3)
        
        # 绘制棋子
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:  # X
                    pygame.draw.line(screen, RED, 
                                    (self.board_start_x + j * self.cell_size + 30, 
                                    self.board_start_y + i * self.cell_size + 30),
                                    (self.board_start_x + (j+1) * self.cell_size - 30, 
                                    self.board_start_y + (i+1) * self.cell_size - 30),
                                    5)
                    pygame.draw.line(screen, RED, 
                                    (self.board_start_x + (j+1) * self.cell_size - 30, 
                                    self.board_start_y + i * self.cell_size + 30),
                                    (self.board_start_x + j * self.cell_size + 30, 
                                    self.board_start_y + (i+1) * self.cell_size - 30),
                                    5)
                elif self.board[i][j] == 2:  # O
                    pygame.draw.circle(screen, BLUE, 
                                    (self.board_start_x + j * self.cell_size + self.cell_size // 2, 
                                    self.board_start_y + i * self.cell_size + self.cell_size // 2),
                                    self.cell_size // 2 - 30,
                                    5)
        
        # 显示当前玩家
        if not self.game_over:
            if self.current_player == 1:
                turn_text = game_font.render("你的回合 (X)", True, WHITE)
            else:
                turn_text = game_font.render("电脑回合 (O)", True, WHITE)
            screen.blit(turn_text, (SCREEN_WIDTH // 2 - 100, 50))
    
    def show_game_over(self):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        if self.winner == 1:
            result_text = game_font.render("你赢了！", True, GREEN)
        elif self.winner == 2:
            result_text = game_font.render("电脑赢了！", True, RED)
        else:
            result_text = game_font.render("平局！", True, YELLOW)
        
        retry_text = game_font.render("按R重试，按ESC返回", True, WHITE)
        
        screen.blit(result_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return

# 数字拼图游戏类
class PuzzleGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.size = 4  # 4x4 拼图
        self.cell_size = 120
        self.puzzle_start_x = (SCREEN_WIDTH - self.cell_size * self.size) // 2
        self.puzzle_start_y = (SCREEN_HEIGHT - self.cell_size * self.size) // 2
        
        # 创建初始拼图（已解决状态）
        self.puzzle = [[i * self.size + j + 1 for j in range(self.size)] for i in range(self.size)]
        self.puzzle[self.size-1][self.size-1] = 0  # 空白格子
        
        # 记录空白格子位置
        self.empty_row = self.size - 1
        self.empty_col = self.size - 1
        
        # 打乱拼图
        self.shuffle()
        
        self.moves = 0
        self.game_over = False
    
    def shuffle(self):
        # 通过随机移动来打乱拼图
        import random
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        
        # 执行1000次随机移动
        for _ in range(1000):
            # 找到可移动的方向
            valid_moves = []
            for dr, dc in directions:
                new_row, new_col = self.empty_row + dr, self.empty_col + dc
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    valid_moves.append((dr, dc))
            
            if valid_moves:
                dr, dc = random.choice(valid_moves)
                # 交换空白格子和相邻格子
                self.puzzle[self.empty_row][self.empty_col] = self.puzzle[self.empty_row + dr][self.empty_col + dc]
                self.puzzle[self.empty_row + dr][self.empty_col + dc] = 0
                # 更新空白格子位置
                self.empty_row += dr
                self.empty_col += dc
    
    def handle_event(self, event):
        """处理单个事件，由GameManager传递"""
        if self.game_over:
            # 游戏结束状态下的按键处理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
        else:
            # 游戏进行中的事件处理
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 鼠标点击
                x, y = pygame.mouse.get_pos()
                row = (y - self.puzzle_start_y) // self.cell_size
                col = (x - self.puzzle_start_x) // self.cell_size
                
                # 检查是否点击在拼图范围内
                if 0 <= row < self.size and 0 <= col < self.size:
                    # 检查是否与空白格子相邻
                    if (abs(row - self.empty_row) == 1 and col == self.empty_col) or \
                       (abs(col - self.empty_col) == 1 and row == self.empty_row):
                        # 交换位置
                        self.puzzle[self.empty_row][self.empty_col] = self.puzzle[row][col]
                        self.puzzle[row][col] = 0
                        # 更新空白格子位置
                        self.empty_row, self.empty_col = row, col
                        self.moves += 1
            elif event.type == pygame.KEYDOWN:
                # 键盘控制
                row, col = self.empty_row, self.empty_col
                if event.key == pygame.K_UP and row < self.size - 1:
                    row += 1
                elif event.key == pygame.K_DOWN and row > 0:
                    row -= 1
                elif event.key == pygame.K_LEFT and col < self.size - 1:
                    col += 1
                elif event.key == pygame.K_RIGHT and col > 0:
                    col -= 1
                
                if (row, col) != (self.empty_row, self.empty_col):
                    # 交换位置
                    self.puzzle[self.empty_row][self.empty_col] = self.puzzle[row][col]
                    self.puzzle[row][col] = 0
                    # 更新空白格子位置
                    self.empty_row, self.empty_col = row, col
                    self.moves += 1
    
    def run(self):
        # 检查是否完成
        if not self.game_over and self.check_win():
            self.game_over = True
        
        # 绘制游戏
        if self.game_over:
            self.show_game_over()
        else:
            self.draw()
    
    def check_win(self):
        # 检查是否按顺序排列
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # 最后一个格子应该是0
                    if self.puzzle[i][j] != 0:
                        return False
                else:
                    # 其他格子应该按顺序排列
                    if self.puzzle[i][j] != i * self.size + j + 1:
                        return False
        return True
    
    def draw(self):
        screen.fill(BLACK)
        
        # 绘制拼图
        for i in range(self.size):
            for j in range(self.size):
                value = self.puzzle[i][j]
                x = self.puzzle_start_x + j * self.cell_size
                y = self.puzzle_start_y + i * self.cell_size
                
                if value != 0:
                    # 绘制数字方块
                    pygame.draw.rect(screen, BLUE, (x, y, self.cell_size - 2, self.cell_size - 2))
                    text = game_font.render(str(value), True, WHITE)
                    text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    screen.blit(text, text_rect)
                else:
                    # 绘制空白格子
                    pygame.draw.rect(screen, (50, 50, 50), (x, y, self.cell_size - 2, self.cell_size - 2))
        
        # 显示移动次数
        moves_text = game_font.render(f"步数: {self.moves}", True, WHITE)
        screen.blit(moves_text, (20, 20))
        
        # 显示提示
        hint_text = game_font.render("点击数字方块或使用方向键移动", True, WHITE)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50))
    
    def show_game_over(self):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        win_text = game_font.render("恭喜你完成拼图！", True, GREEN)
        moves_text = game_font.render(f"总步数: {self.moves}", True, WHITE)
        retry_text = game_font.render("按R重试，按ESC返回", True, WHITE)
        
        screen.blit(win_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 80))
        screen.blit(moves_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 20))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 40))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return

# 2048游戏类
class Game2048:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.size = 4  # 4x4 棋盘
        self.cell_size = 120
        self.board_start_x = (SCREEN_WIDTH - self.cell_size * self.size) // 2
        self.board_start_y = (SCREEN_HEIGHT - self.cell_size * self.size) // 2
        
        # 创建空白棋盘
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # 初始化两个数字
        self.add_new_number()
        self.add_new_number()
        
        self.score = 0
        self.game_over = False
        self.victory = False
    
    def add_new_number(self):
        # 找到所有空白位置
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            import random
            i, j = random.choice(empty_cells)
            # 90%概率生成2，10%概率生成4
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            
            # 检查是否获胜
            if self.board[i][j] == 2048:
                self.victory = True
    
    def handle_event(self, event):
        """处理单个事件，由GameManager传递"""
        if self.game_over:
            # 游戏结束状态下的按键处理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
        elif not self.victory:
            # 游戏进行中的事件处理
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP:
                    moved = self.move_up()
                elif event.key == pygame.K_DOWN:
                    moved = self.move_down()
                elif event.key == pygame.K_LEFT:
                    moved = self.move_left()
                elif event.key == pygame.K_RIGHT:
                    moved = self.move_right()
                elif event.key == pygame.K_r:
                    self.reset()
                
                # 如果有移动，添加新数字
                if moved:
                    self.add_new_number()
        else:
            # 胜利状态下的按键处理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
    
    def run(self):
        # 检查游戏是否结束
        if not self.game_over and not self.can_move():
            self.game_over = True
        
        # 绘制游戏
        if self.game_over:
            self.show_game_over()
        else:
            self.draw()
    
    def move_left(self):
        moved = False
        for i in range(self.size):
            # 压缩行
            new_row = [num for num in self.board[i] if num != 0]
            
            # 合并相同数字
            j = 0
            while j < len(new_row) - 1:
                if new_row[j] == new_row[j + 1]:
                    new_row[j] *= 2
                    self.score += new_row[j]
                    del new_row[j + 1]
                else:
                    j += 1
            
            # 填充空白
            while len(new_row) < self.size:
                new_row.append(0)
            
            # 检查是否有变化
            if new_row != self.board[i]:
                self.board[i] = new_row
                moved = True
        
        return moved
    
    def move_right(self):
        # 反转每一行，使用向左移动，再反转回来
        for i in range(self.size):
            self.board[i] = self.board[i][::-1]
        
        moved = self.move_left()
        
        # 反转回来
        for i in range(self.size):
            self.board[i] = self.board[i][::-1]
        
        return moved
    
    def move_up(self):
        # 转置棋盘，使用向左移动，再转置回来
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved
    
    def move_down(self):
        # 转置棋盘，使用向右移动，再转置回来
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved
    
    def transpose(self):
        # 转置棋盘（行变列，列变行）
        self.board = [list(row) for row in zip(*self.board)]
    
    def can_move(self):
        # 检查是否有空白位置
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return True
        
        # 检查是否有相邻相同数字
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
        
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.board[i][j] == self.board[i + 1][j]:
                    return True
        
        return False
    
    def get_cell_color(self, value):
        # 根据数值返回对应的颜色
        colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        return colors.get(value, (60, 58, 50))
    
    def get_text_color(self, value):
        # 返回文字颜色（深色或白色）
        return (249, 246, 242) if value >= 8 else (119, 110, 101)
    
    def draw(self):
        screen.fill((187, 173, 160))
        
        # 绘制得分
        score_text = game_font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # 绘制棋盘边框
        pygame.draw.rect(screen, (119, 110, 101), 
                        (self.board_start_x - 10, self.board_start_y - 10, 
                        self.cell_size * self.size + 20, 
                        self.cell_size * self.size + 20), 0, 10)
        
        # 绘制单元格
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                x = self.board_start_x + j * self.cell_size
                y = self.board_start_y + i * self.cell_size
                
                # 绘制单元格背景
                cell_color = self.get_cell_color(value)
                pygame.draw.rect(screen, cell_color, 
                                (x, y, self.cell_size - 10, self.cell_size - 10), 0, 5)
                
                # 绘制数字
                if value != 0:
                    # 根据数值调整字体大小
                    if value < 100:
                        font_size = 40
                    elif value < 1000:
                        font_size = 35
                    else:
                        font_size = 30
                    
                    try:
                        number_font = pygame.font.SysFont(font_options[0], font_size, bold=True)
                    except:
                        number_font = pygame.font.SysFont(None, font_size, bold=True)
                    
                    text_color = self.get_text_color(value)
                    text = number_font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=(x + (self.cell_size - 10) // 2, 
                                                    y + (self.cell_size - 10) // 2))
                    screen.blit(text, text_rect)
        
        # 如果获胜，显示胜利消息
        if self.victory and not self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))  # 半透明白色
            screen.blit(overlay, (0, 0))
            
            win_text = game_font.render("你达到了2048！", True, (119, 110, 101))
            continue_text = game_font.render("继续游戏还是按R重新开始？", True, (119, 110, 101))
            
            screen.blit(win_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 50))
            screen.blit(continue_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 20))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
    
    def show_game_over(self):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        # 使用render_text函数渲染文本以确保中文正确显示
        game_over_text = render_text("游戏结束！", game_font, WHITE)
        score_text = render_text(f"最终分数: {self.score}", game_font, WHITE)
        retry_text = render_text("按R重试", game_font, WHITE)
        
        # 居中显示文本
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - retry_text.get_width()//2, SCREEN_HEIGHT//2 + 40))

# 猜数字游戏类
class GuessNumberGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        import random
        self.target_number = random.randint(1, 100)
        self.guesses = []
        self.max_guesses = 10
        self.game_over = False
        self.won = False
        self.current_guess = ""
    
    def run(self):
        # 绘制游戏
        if self.game_over:
            self.show_game_over()
        else:
            self.draw()
    
    def handle_event(self, event):
        """处理单个事件，由GameManager传递"""
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                # 游戏结束状态下的按键处理
                if event.key == pygame.K_r:
                    self.reset()
            else:
                # 游戏进行中的按键处理
                if event.key == pygame.K_RETURN and self.current_guess:
                    # 提交猜测
                    try:
                        guess = int(self.current_guess)
                        if 1 <= guess <= 100:
                            self.guesses.append(guess)
                            
                            # 检查是否猜对
                            if guess == self.target_number:
                                self.game_over = True
                                self.won = True
                            elif len(self.guesses) >= self.max_guesses:
                                self.game_over = True
                                self.won = False
                            
                            self.current_guess = ""
                    except ValueError:
                        self.current_guess = ""
                elif event.key == pygame.K_BACKSPACE:
                    # 删除最后一个字符
                    self.current_guess = self.current_guess[:-1]
                elif event.unicode.isdigit():
                    # 添加数字
                    if len(self.current_guess) < 3:  # 最多3位数字
                        self.current_guess += event.unicode
    
    def draw(self):
        # 创建渐变背景
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            r = int(0 + (20 - 0) * y / SCREEN_HEIGHT)
            g = int(0 + (20 - 0) * y / SCREEN_HEIGHT)
            b = int(0 + (40 - 0) * y / SCREEN_HEIGHT)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        screen.blit(background, (0, 0))
        
        # 绘制标题，使用新的渲染函数
        title = render_text("猜数字游戏", WHITE, 48)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # 创建信息面板
        info_panel = pygame.Rect(SCREEN_WIDTH//2 - 300, 150, 600, 500)
        pygame.draw.rect(screen, (50, 50, 70), info_panel, 0, 10)
        pygame.draw.rect(screen, (100, 100, 120), info_panel, 2, 10)
        
        # 绘制游戏说明
        instructions = [
            "我想了一个1到100之间的数字",
            f"你有{self.max_guesses - len(self.guesses)}次机会猜测",
            "输入一个数字并按回车"
        ]
        
        for i, text in enumerate(instructions):
            instruction_text = render_text(text, WHITE, 28)
            text_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 200 + i * 50))
            screen.blit(instruction_text, text_rect)
        
        # 绘制当前输入框
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 200, 350, 400, 60)
        pygame.draw.rect(screen, (70, 70, 90), input_box, 0, 8)
        pygame.draw.rect(screen, (120, 120, 140), input_box, 2, 8)
        
        # 绘制当前输入
        guess_text = render_text(f"你的猜测: {self.current_guess}", YELLOW, 32)
        guess_rect = guess_text.get_rect(center=input_box.center)
        screen.blit(guess_text, guess_rect)
        
        # 绘制历史猜测标题
        history_title = render_text("历史猜测:", WHITE, 30)
        history_title_rect = history_title.get_rect(center=(SCREEN_WIDTH//2, 450))
        screen.blit(history_title, history_title_rect)
        
        # 绘制历史猜测，限制显示数量避免溢出
        max_display_guesses = 5  # 最多显示5条记录
        start_index = max(0, len(self.guesses) - max_display_guesses)
        
        for i, guess in enumerate(self.guesses[start_index:], start=start_index):
            display_index = i - start_index
            if guess < self.target_number:
                result = "太小了！"
                color = BLUE
            elif guess > self.target_number:
                result = "太大了！"
                color = RED
            else:
                result = "猜对了！"
                color = GREEN
            
            guess_history = render_text(f"{guess} - {result}", color, 24)
            history_rect = guess_history.get_rect(center=(SCREEN_WIDTH//2, 490 + display_index * 35))
            screen.blit(guess_history, history_rect)
    
    def show_game_over(self):
        # 创建渐变背景
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            r = int(0 + (20 - 0) * y / SCREEN_HEIGHT)
            g = int(0 + (20 - 0) * y / SCREEN_HEIGHT)
            b = int(0 + (40 - 0) * y / SCREEN_HEIGHT)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        screen.blit(background, (0, 0))
        
        # 创建结果面板
        result_panel = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 150, 600, 300)
        pygame.draw.rect(screen, (50, 50, 70), result_panel, 0, 10)
        pygame.draw.rect(screen, (100, 100, 120), result_panel, 2, 10)
        
        # 绘制结果文本
        if self.won:
            result_text = render_text("恭喜你猜对了！", GREEN, 48)
        else:
            result_text = render_text(f"游戏结束！正确数字是 {self.target_number}", RED, 40)
        
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(result_text, result_rect)
        
        attempts_text = render_text(f"你用了 {len(self.guesses)} 次尝试", WHITE, 32)
        attempts_rect = attempts_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
        screen.blit(attempts_text, attempts_rect)
        
        retry_text = render_text("按R重试，按ESC返回", YELLOW, 28)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        screen.blit(retry_text, retry_rect)

# 主游戏循环
def main():
    game_manager = GameManager()
    
    running = True
    while running:
        clock.tick(FPS)
        
        # 处理事件
        if not game_manager.handle_events():
            running = False
        
        # 渲染当前状态
        if game_manager.state == "menu":
            game_manager.run_menu()
        elif game_manager.state == "game":
            game_manager.run_game()
        
        # 更新屏幕
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()