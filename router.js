/**
 * DDoSeek 系统路由管理器
 * 负责页面导航、身份验证、用户交互等功能
 */
class DDoSeekRouter {
    constructor(currentPage = 'dashboard') {
        this.currentPage = currentPage;
        this.pauseUpdates = false;
        this.init();
    }

    init() {
        // 检查登录状态
        this.checkAuthentication();
        
        // 设置页面标题
        this.setPageTitle();
        
        // 添加导航事件监听
        this.bindNavigationEvents();
        
        // 添加键盘快捷键
        this.bindKeyboardShortcuts();
        
        // 初始化用户界面
        this.initUserInterface();
        
        // 监听页面可见性变化
        this.bindVisibilityChange();
    }

    checkAuthentication() {
        const isLoggedIn = localStorage.getItem('DDoSeek_logged_in');
        const loginTime = localStorage.getItem('DDoSeek_login_time');
        
        if (!isLoggedIn) {
            // 如果未登录，跳转到登录页面
            if (window.location.pathname !== '/login.html' && !window.location.pathname.endsWith('login.html')) {
                window.location.href = 'login.html';
            }
            return false;
        }
        
        // 检查登录是否过期（24小时）
        if (loginTime && (new Date().getTime() - parseInt(loginTime)) > 24 * 60 * 60 * 1000) {
            this.logout();
            return false;
        }
        
        // 登录成功后，如果没有指定页面，默认跳转到DDoS检测防护页面
        if (isLoggedIn && window.location.pathname.endsWith('login.html')) {
            window.location.href = 'ddos-detection.html';
            return true;
        }
        
        return true;
    }

    setPageTitle() {
        const pageTitles = {
            'dashboard': '系统仪表盘',
            'network-monitor': '网络监测中心',
            'ddos-detection': 'DDoS检测防护',
            'firewall-management': '防火墙管理',
            'log-center': '智能日志中心',
            'deepseek-assistant': 'DeepSeek AI助手',
            'rule-config': '规则配置中心',
            'system-test': '系统测试平台',
            'login': '登录认证'
        };
        
        const title = pageTitles[this.currentPage] || 'DDoSeek';
        document.title = `DDoSeek - ${title}`;
    }

    bindNavigationEvents() {
        // 侧边栏导航点击事件
        document.querySelectorAll('.sidebar-menu a').forEach(link => {
            link.addEventListener('click', (e) => {
                // 移除所有活跃状态
                document.querySelectorAll('.sidebar-menu a').forEach(l => l.classList.remove('active'));
                // 添加活跃状态到当前链接
                e.target.closest('a').classList.add('active');
                
                // 保存当前页面状态
                const href = e.target.closest('a').getAttribute('href');
                const pageName = href.replace('.html', '');
                localStorage.setItem('DDoSeek_current_page', pageName);
                
                // 添加页面切换动画
                this.addPageTransition();
            });
        });

        // 用户头像点击事件
        const userAvatar = document.querySelector('.user-avatar');
        if (userAvatar) {
            userAvatar.addEventListener('click', () => {
                this.showUserMenu();
            });
        }

        // 通知铃铛点击事件
        const bellIcon = document.querySelector('.fa-bell');
        if (bellIcon) {
            bellIcon.addEventListener('click', () => {
                this.showNotifications();
            });
        }

        // Logo点击返回首页（DDoS检测防护页面）
        const logo = document.querySelector('.logo');
        if (logo) {
            logo.addEventListener('click', () => {
                window.location.href = 'ddos-detection.html';
            });
            logo.style.cursor = 'pointer';
        }
    }

    bindKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + 数字键快速导航 (按新的导航顺序)
            if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '8') {
                e.preventDefault();
                const navigationMap = {
                    '1': 'ddos-detection.html',      // DDoS检测防护
                    '2': 'deepseek-assistant.html',  // DeepSeek AI助手  
                    '3': 'dashboard.html',           // 系统仪表盘
                    '4': 'network-monitor.html',     // 网络监测中心
                    '5': 'firewall-management.html', // 防火墙管理
                    '6': 'log-center.html',          // 智能日志中心
                    '7': 'rule-config.html',         // 规则配置中心
                    '8': 'system-test.html'          // 系统测试平台
                };
                
                const targetPage = navigationMap[e.key];
                if (targetPage) {
                    window.location.href = targetPage;
                }
            }
            
            // ESC键返回DDoS检测防护页面（新的默认首页）
            if (e.key === 'Escape') {
                window.location.href = 'ddos-detection.html';
            }
            
            // Ctrl/Cmd + Shift + L 快速退出
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'L') {
                e.preventDefault();
                this.logout();
            }
            
            // F5 或 Ctrl/Cmd + R 刷新页面
            if (e.key === 'F5' || ((e.ctrlKey || e.metaKey) && e.key === 'r')) {
                // 保存刷新前的状态
                localStorage.setItem('DDoSeek_last_refresh', new Date().getTime());
            }
        });
    }

    initUserInterface() {
        // 显示用户信息
        const username = localStorage.getItem('DDoSeek_username') || '管理员';
        const userNameSpan = document.querySelector('.user-section span');
        if (userNameSpan) {
            userNameSpan.textContent = username;
        }
        
        // 添加快捷键提示
        this.addKeyboardHints();
        
        // 添加页面加载动画
        this.addPageLoadAnimation();
    }

    addKeyboardHints() {
        // 在页面底部添加快捷键提示
        const hints = document.createElement('div');
        hints.style.cssText = `
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 11px;
            z-index: 999;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        `;
        
        hints.innerHTML = `
            <span>快捷键：</span>
            <span style="margin: 0 8px;">Ctrl+1 DDoS防护</span>
            <span style="margin: 0 8px;">Ctrl+2 AI助手</span>
            <span style="margin: 0 8px;">ESC 返回首页</span>
            <span style="margin: 0 8px;">Ctrl+Shift+L 退出</span>
        `;
        
        document.body.appendChild(hints);
        
        // 5秒后显示提示，10秒后隐藏
        setTimeout(() => {
            hints.style.opacity = '1';
            setTimeout(() => {
                hints.style.opacity = '0';
                setTimeout(() => {
                    if (document.body.contains(hints)) {
                        document.body.removeChild(hints);
                    }
                }, 300);
            }, 5000);
        }, 2000);
    }

    addPageLoadAnimation() {
        // 添加页面加载动画
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                mainContent.style.transition = 'all 0.5s ease';
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    addPageTransition() {
        // 添加页面切换动画效果
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #3182ce, #667eea);
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        `;
        
        overlay.innerHTML = `
            <div style="text-align: center;">
                <div style="width: 40px; height: 40px; border: 3px solid rgba(255,255,255,0.3); border-top: 3px solid white; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px;"></div>
                <div>页面切换中...</div>
            </div>
        `;
        
        // 添加旋转动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 10);
    }

    showUserMenu() {
        // 移除已存在的菜单
        const existingMenu = document.querySelector('.user-menu');
        if (existingMenu) {
            document.body.removeChild(existingMenu);
            return;
        }

        const menu = document.createElement('div');
        menu.className = 'user-menu';
        menu.style.cssText = `
            position: fixed;
            top: 60px;
            right: 20px;
            background: white;
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            min-width: 180px;
            padding: 8px 0;
            animation: slideInRight 0.3s ease;
        `;
        
        const username = localStorage.getItem('DDoSeek_username') || '管理员';
        const loginTime = localStorage.getItem('DDoSeek_login_time');
        const loginDate = loginTime ? new Date(parseInt(loginTime)).toLocaleString() : '未知';
        
        menu.innerHTML = `
            <div style="padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.1); background: rgba(49,130,206,0.05);">
                <div style="font-weight: 600; color: #2d3748;">${username}</div>
                <div style="font-size: 11px; color: #718096; margin-top: 2px;">登录时间：${loginDate}</div>
            </div>
            <div style="padding: 8px 16px; cursor: pointer; font-size: 14px; transition: background 0.3s ease;" onmouseover="this.style.background='rgba(49,130,206,0.05)'" onmouseout="this.style.background='transparent'" onclick="router.showProfile()">
                <i class="fas fa-user" style="width: 16px; margin-right: 8px;"></i> 个人资料
            </div>
            <div style="padding: 8px 16px; cursor: pointer; font-size: 14px; transition: background 0.3s ease;" onmouseover="this.style.background='rgba(49,130,206,0.05)'" onmouseout="this.style.background='transparent'" onclick="router.showSettings()">
                <i class="fas fa-cog" style="width: 16px; margin-right: 8px;"></i> 系统设置
            </div>
            <div style="padding: 8px 16px; cursor: pointer; font-size: 14px; transition: background 0.3s ease;" onmouseover="this.style.background='rgba(49,130,206,0.05)'" onmouseout="this.style.background='transparent'" onclick="router.showHelp()">
                <i class="fas fa-question-circle" style="width: 16px; margin-right: 8px;"></i> 帮助中心
            </div>
            <div style="border-top: 1px solid rgba(0,0,0,0.1); margin: 4px 0;"></div>
            <div style="padding: 8px 16px; cursor: pointer; font-size: 14px; color: #e53e3e; transition: background 0.3s ease;" onmouseover="this.style.background='rgba(229,62,62,0.05)'" onmouseout="this.style.background='transparent'" onclick="router.logout()">
                <i class="fas fa-sign-out-alt" style="width: 16px; margin-right: 8px;"></i> 退出登录
            </div>
        `;
        
        document.body.appendChild(menu);
        
        // 点击其他地方关闭菜单
        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!menu.contains(e.target) && !e.target.closest('.user-avatar')) {
                    document.body.removeChild(menu);
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 100);
    }

    showNotifications() {
        // 移除已存在的通知面板
        const existingNotifications = document.querySelector('.notifications-panel');
        if (existingNotifications) {
            document.body.removeChild(existingNotifications);
            return;
        }

        const notifications = document.createElement('div');
        notifications.className = 'notifications-panel';
        notifications.style.cssText = `
            position: fixed;
            top: 60px;
            right: 60px;
            background: white;
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            width: 320px;
            max-height: 450px;
            overflow-y: auto;
            animation: slideInRight 0.3s ease;
        `;
        
        // 获取通知数据
        const notificationData = this.getNotifications();
        
        notifications.innerHTML = `
            <div style="padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.1); font-weight: 600; display: flex; justify-content: space-between; align-items: center;">
                <span>系统通知</span>
                <span style="background: #e53e3e; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">${notificationData.length}</span>
            </div>
            ${notificationData.map(notification => `
                <div style="padding: 12px 16px; border-bottom: 1px solid rgba(0,0,0,0.1); font-size: 13px; cursor: pointer; transition: background 0.3s ease;" onmouseover="this.style.background='rgba(0,0,0,0.03)'" onmouseout="this.style.background='transparent'">
                    <div style="color: ${notification.color}; font-weight: 500; display: flex; align-items: center; gap: 6px;">
                        <i class="${notification.icon}"></i>
                        ${notification.title}
                    </div>
                    <div style="color: #718096; margin-top: 4px; line-height: 1.4;">${notification.message}</div>
                    <div style="color: #a0aec0; font-size: 11px; margin-top: 4px;">${notification.time}</div>
                </div>
            `).join('')}
            <div style="padding: 12px 16px; text-align: center; border-top: 1px solid rgba(0,0,0,0.1);">
                <a href="log-center.html" style="color: #3182ce; text-decoration: none; font-size: 12px; font-weight: 500;">查看所有通知</a>
            </div>
        `;
        
        document.body.appendChild(notifications);
        
        // 点击其他地方关闭通知
        setTimeout(() => {
            document.addEventListener('click', function closeNotifications(e) {
                if (!notifications.contains(e.target) && !e.target.closest('.fa-bell')) {
                    document.body.removeChild(notifications);
                    document.removeEventListener('click', closeNotifications);
                }
            });
        }, 100);
    }

    getNotifications() {
        // 模拟获取通知数据
        return [
            {
                title: '高危威胁',
                message: '检测到来自多个IP的大规模DDoS攻击，已自动启动防护措施',
                time: '2分钟前',
                color: '#e53e3e',
                icon: 'fas fa-exclamation-triangle'
            },
            {
                title: '系统警告',
                message: '内存使用率超过85%，建议进行系统优化或扩容',
                time: '5分钟前',
                color: '#d69e2e',
                icon: 'fas fa-exclamation'
            },
            {
                title: '防护更新',
                message: 'AI防护模型已更新至v2.1.3，检测准确率提升至99.2%',
                time: '10分钟前',
                color: '#38a169',
                icon: 'fas fa-shield-check'
            },
            {
                title: '系统信息',
                message: '定时备份任务已完成，数据已安全保存至云端存储',
                time: '15分钟前',
                color: '#3182ce',
                icon: 'fas fa-info-circle'
            },
            {
                title: '网络状态',
                message: '所有网络节点运行正常，平均响应时间12ms',
                time: '20分钟前',
                color: '#38a169',
                icon: 'fas fa-network-wired'
            }
        ];
    }

    showProfile() {
        alert('个人资料功能开发中...');
    }

    showSettings() {
        alert('系统设置功能开发中...');
    }

    showHelp() {
        window.open('https://DDoSeek.com/help', '_blank');
    }

    logout() {
        if (confirm('确定要退出登录吗？')) {
            // 清除登录状态
            localStorage.removeItem('DDoSeek_logged_in');
            localStorage.removeItem('DDoSeek_username');
            localStorage.removeItem('DDoSeek_remember');
            localStorage.removeItem('DDoSeek_current_page');
            localStorage.removeItem('DDoSeek_login_time');
            
            // 添加退出动画
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #e53e3e, #c53030);
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 18px;
            `;
            
            overlay.innerHTML = `
                <div style="text-align: center;">
                    <i class="fas fa-sign-out-alt" style="font-size: 48px; margin-bottom: 16px;"></i>
                    <div>正在退出系统...</div>
                </div>
            `;
            
            document.body.appendChild(overlay);
            
            setTimeout(() => {
                overlay.style.opacity = '1';
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 1000);
            }, 10);
        }
    }

    bindVisibilityChange() {
        document.addEventListener('visibilitychange', () => {
            this.handleVisibilityChange();
        });
    }

    handleVisibilityChange() {
        if (document.hidden) {
            // 页面隐藏时暂停数据更新
            this.pauseUpdates = true;
            console.log('页面隐藏，暂停数据更新');
        } else {
            // 页面显示时恢复数据更新
            this.pauseUpdates = false;
            console.log('页面显示，恢复数据更新');
            
            // 重新检查认证状态
            this.checkAuthentication();
        }
    }

    // 工具方法：显示消息提示
    showMessage(message, type = 'info', duration = 3000) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#38a169' : type === 'error' ? '#e53e3e' : type === 'warning' ? '#d69e2e' : '#3182ce'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            font-size: 14px;
            max-width: 300px;
            word-wrap: break-word;
            animation: slideInRight 0.3s ease;
        `;
        
        messageDiv.textContent = message;
        document.body.appendChild(messageDiv);
        
        // 自动移除
        setTimeout(() => {
            messageDiv.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(messageDiv)) {
                    document.body.removeChild(messageDiv);
                }
            }, 300);
        }, duration);
    }
}

// 添加CSS动画
if (!document.querySelector('#router-animations')) {
    const style = document.createElement('style');
    style.id = 'router-animations';
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideInDown {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// 导出路由管理器（如果支持ES6模块）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DDoSeekRouter;
} 