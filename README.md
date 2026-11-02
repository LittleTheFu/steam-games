# Steam 游戏游玩时间页面

## 发布到 GitHub Pages

1. 在 GitHub 新建一个仓库，例如 `steam-games`。
2. 上传本目录中的 `index.html` 和 `games.csv`。
3. 打开仓库的 **Settings → Pages**，在 **Build and deployment** 中选择 **Deploy from a branch**，选 `main` 分支和 `/(root)`，保存。
4. 等待 Pages 部署完成后，页面地址会显示在 Pages 设置中，形式类似 `https://你的用户名.github.io/steam-games/`。

GitHub Free 需要公开仓库才能使用 Pages；发布出来的页面也会公开。上传前请确认愿意公开游戏清单和游玩时间。

## 更新数据

用新的 Steam 游戏 CSV 覆盖 `games.csv` 并提交到仓库，网页会读取最新数据。CSV 表头需要是 `Game,Hours Played,App ID`。

游戏图片通过 Steam 商店静态图片地址按 App ID 加载。若某张图片不可用，页面会自动显示游戏名称首字母作为占位图。



## Automatic Steam sync

The GitHub Actions workflow syncs the library daily at 18:00 UTC (02:00 China Standard Time) and can also be run manually from the Actions tab. Before it can run, add a repository Actions secret named `STEAM_API_KEY` containing your Steam Web API key. The workflow fetches the public game details for the configured SteamID and updates `games.csv`; the page then shows Steam's game icons when available.
