import pymysql

class ParagraphPipeline:
    conn = pymysql.connect(
        host='localhost',
        user="root",
        passwd="root",
        autocommit=True
    )
    cursor = conn.cursor()
    paragraph_lis = []
    def process_item(self, item, spider):
        sql = "INSERT INTO `paragraphdatabase`.`tb_keyparagraph_selfsites_content` (`paragraph`, `tag_ori`) VALUES (\'{}\',\'{}\');".format(
            item['paragraph'],
            item['tag_ori'],
        )
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(sql)
        self.paragraph_lis.append(item['paragraph'])
        return item


    def close_spider(self, spider):
        # �ر����ݿ�
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print("�ر����ݿ�����ʧ��")
            pass
        print("- վ�㣺{} ; ��ȡ���ͣ�{}; ����������{};".format(spider.name, 'keyparagraph', len(self.paragraph_lis)))