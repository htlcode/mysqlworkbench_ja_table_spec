# MySQL Workbench テーブル定義書 HTML出力プラグイン

このプラグインは、MySQL Workbenchで作成したER図から、データベースのテーブル定義書を日本語でHTML形式で自動生成するためスクリプトです。  
テーブルやカラムの情報を整理されたHTMLファイルとして出力できるので、設計書やドキュメント作成に便利です。

tmsanchezのリポからフォークされ、アレンジしています。

## プラグインのインストール・アンインストール方法

### インストール方法

1. MySQL Workbenchのメニューから **Scripting > Install Plugin/Module** を選択します。
2. インストール後、MySQL Workbenchを再起動してください。
3. 再起動後、**Tools/Catalog** メニューに **Generate tables definition HTML** が表示されます。
4. ER図を開いてプラグインを実行すると、HTMLファイルが作成されます。

### アンインストール方法

1. MySQL Workbenchのメニューから **Scripting > Plugin Manager** を選択します。
2. プラグインを選択し、**Uninstall** をクリックします。
