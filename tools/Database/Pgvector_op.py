import psycopg2

# FIXME 还未开始修改文件内容，才复制过来的

# pgvector操作类，封装操作，隐私项保存在config.ini文件里，自行修改

class Pgvector:
    def __init__(self,host,port,database,user,password,table,mode:str='CHAT'):
        self.mode = "RAG" if mode == "RAG" else "CHAT"
        self.table = table
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cur = self.conn.cursor()

    # 创建表
    def creat_table(self):
        if self.mode == "RAG":
            self.cur.execute(f'''
                            CREATE TABLE IF NOT EXISTS {self.table}(
                            id SERIAL PRIMARY KEY,
                            document VARCHAR,
                            embedding vector(1), 
                            doc_name VARCHAR,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                        ''')
        elif self.mode == "CHAT":
            self.cur.execute(f'''
                            CREATE TABLE IF NOT EXISTS {self.table}(
                            id SERIAL PRIMARY KEY,
                            uuid VARCHAR,
                            input VARCHAR,
                            answer VARCHAR,
                            chats_user vector(1),
                            chats_ai vector(1),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                        ''')
        else:
            print("创建模式有误，检查参数对象mode属性是否符合要求")
        # 提交事务
        self.conn.commit()



    # 原生方式查询
    def select(self,p):
        cur = self.conn.cursor()
        if self.mode == "RAG":
            embed = p
            cur.execute(f'''SELECT * FROM {self.table} ORDER BY embedding <-> '{str(embed)}' LIMIT 3;''')
        elif self.mode == "CHAT":
            uuid = p
            # TODO    没有根据时间查询，最近期的记录返回而是返回全部记录，可能导致上下文过长，可以考虑总结后返回
            cur.execute(f'''SELECT input,answer FROM {self.table} WHERE uuid = '{uuid}' ORDER BY created_at DESC LIMIT 10''')
        else:
            print("创建模式有误，检查参数对象mode属性是否符合要求")
        return cur.fetchall()


    def insert(self,data):
        if self.mode == "RAG":
            # 插入多条数据
            # data = [
            #     ('Item1', [0.1, 0.2, 0.3, 0.4], 'dfasf.md'),  # 128维向量
            #     ('Item2', [0.5, 0.6, 0.7, 0.8], 'dl.txt'),
            #     ('Item3', [0.9, 1.0, 1.1, 1.2], 'k.txt')
            # ]
            values_str = ','.join(self.cur.mogrify("(%s, %s, %s)", row).decode("utf-8") for row in data)
            insert_query = f"INSERT INTO {self.table} (document, embedding, doc_name) VALUES {values_str}"
            # 执行批量插入
            self.cur.execute(insert_query)
        elif self.mode == "CHAT":
            values_str = ','.join(self.cur.mogrify("(%s, %s, %s, %s, %s)", row).decode("utf-8") for row in data)
            insert_query = f"INSERT INTO {self.table} (uuid, input, answer, chats_user, chats_ai) VALUES {values_str}"
            # 执行批量插入
            self.cur.execute(insert_query)
        else:
            print("创建模式有误，检查参数对象mode属性是否符合要求")
        # 提交事务
        self.conn.commit()





if __name__ == '__main__':
    from Transformer_sentence import BegZh
    from Rag_agent import OllamaAgent
    # cf = configparser.ConfigParser()
    # cf.read("../config/config.ini")
    # print(cf.get("RAG", "table"))
    # pg = Pgvector(
    #     cf.get("RAG", "host"),
    #     cf.get("RAG", "port"),
    #     cf.get("RAG", "database"),
    #     cf.get("RAG", "user"),
    #     cf.get("RAG", "password"),
    #     cf.get("RAG", "table"),
    # )
    # pg.creat_rag_table()
    # data = [
    #     ('Item1', '[0.1, 0.2, 0.3, 0.4]', 'dfasf.md'),  # 128维向量
    #     ('Item2', '[0.5, 0.6, 0.7, 0.8]', 'dl.txt'),
    #     ('Item3', '[0.9, 1.0, 1.1, 1.2]', 'k.txt')
    # ]
    # pg.insert(data)
    # beg_zh = BegZh(cf.get("beg_model", "path"))
    #
    # result = pg.select(str(beg_zh.encode("就业训练中心SYBppt路演小组一等奖算吗")))
    # print(result)

    import configparser
    cf = configparser.ConfigParser()
    cf.read("../config/config.ini")
    print(cf.get("CHAT", "table"))
    pg = Pgvector(
        cf.get("CHAT", "host"),
        cf.get("CHAT", "port"),
        cf.get("CHAT", "database"),
        cf.get("CHAT", "user"),
        cf.get("CHAT", "password"),
        cf.get("CHAT", "table"),
        mode="CHAT"
    )
    pg.creat_table()
    beg_zh = BegZh(cf.get("beg_model", "path"))
    oll = OllamaAgent('qwen2.5', 22, 33, False)
    begin_ss = pg.select('21312')

    for i in begin_ss:
        print(i[0])
        oll.memory.save_context({"input": i[0]}, {"output": i[1]})


    while 1:
        pp = input("你有什么想说的：")
        answer = oll.chat(pp)
        e_pp = beg_zh.encode(pp)
        e_answer = beg_zh.encode(answer)
        print(answer)
        data = [
            ('21312',pp,answer,str(e_pp),str(e_answer))
        ]
        pg.insert(data)



