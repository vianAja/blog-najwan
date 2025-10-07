with open('_posts/2024-10-19-openstack.md', encoding='utf-8',) as f:
    data = f.read()
    print(data)
    #print(type(data))

import datetime
import os
os.system('cls')
print(datetime.datetime.date)

#full_path = os.getcwd()
#path_post = os.path.join(full_path, '_posts')

class MainAutoGenerateTemplate:
    def __init__(self):
        global command_name, type_command, command_list
        self.full_path = os.getcwd()
        self.tanggal = datetime.datetime.now().strftime('%Y-%m-%d')
        self.author = 'Najwan Octavian Gerrard'
        self.tags = []
        self.template_code =  '''
- {}
  ```{}
{}
  ```
  ---

'''
        self.template_header = '''---
layout: post
title: {}
subtitle: {}
cover-img: /assets/img/wallpaper2.png
thumbnail-img: https://ant.ncc.asia/wp-content/uploads/2024/05/docker.png
share-img: /assets/img/wallpaper2.png
tags: {}
author: {}
---'''
        self.template_gambar = '![{}](../assets/images/{}{})'
    def JudulCreate(self):
        print('Masukan Nama Postingan Anda :')
        nama_postingan = str(input('\t=> ')).replace(' ','-')
        nama_postingan = 'pass'
        self.nama_file = f'{self.tanggal}-{nama_postingan}.md'
        
        print('Masukan Judul untuk Postingan Anda :')
        self.title = str(input('\t=> '))
        self.title = 'pass'
        
        print('Masukan Deskripsi singkat untuk judul Postingan Anda :')
        self.description = str(input('\t=> '))
        self.description = 'pass'
    
    def addTags(self):
        print('Masukan Tags untuk Postingan anda, beri tanda koma ( , ) untuk tags lain :')
        tags = str(input('\t=> ')).replace(' ','').split(',')
        tags = ['pass', 'pa']
        self.tags = tags
    
    def generateTemplate(self):
        path_file = os.path.join(self.full_path, self.nama_file)
        with open(path_file, 'a') as file:
            ## untuk membuat header awalan
            file.write(str(self.template_header.format(
                self.title,
                self.description,
                self.tags,
                self.author
            )))

    def main(self):
        print(self.tanggal)
        self.JudulCreate()
        self.addTags()
        print(self.nama_file)
        print(self.tags)
        
        self.generateTemplate()

if __name__ == "__main__":
    p = MainAutoGenerateTemplate()
    p.main()