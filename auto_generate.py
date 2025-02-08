with open('_posts/2024-10-19-openstack.md', encoding='utf-8',) as f:
    data = f.read()
    print(data)
    #print(type(data))

import datetime

print(datetime.datetime.date)


class MainAutoGenerateTemplate:
    def __init__(self):
        global command_name, type_command, command_list
        self.tanggal = datetime.datetime.now().strftime('%Y-%m-%d')
        self.title = ''
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
        
        with open(self.nama_file, 'a') as file:
            ## untuk membuat header awalan
            file.write(str(self.template_header.format(
                self.title,
                self.description,
                self.tags,
                self.author
            )))
            i = 1
            ## looping untuk banyaknya instruksi yang akan di jalankan
            while True:
                try:
                    command_list = []
                    print(f'Masukan Langkah ke {i}')
                    command_name = str(input('   => '))
                    type_command = 'bash'
                    
                    ## looping untuk banyaknya command / perintah yang akan di gunakan
                    print(f'Masukan Code block command, klik CTRL + C untuk berhenti')
                    while True:
                        try:
                            command = str(input('   => '))
                            command_list.append(command)
                        except KeyboardInterrupt:
                            print('\n')
                            break
                    i += 1
                    ## untuk membuat instruksi ke markdown
                    file.write(self.template_code.format(
                        command_name,
                        type_command,
                        "".join(["  "+d+"\n" for d in command_list]))
                    )
                except KeyboardInterrupt:
                    break
    def main(self):
        print(self.tanggal)
        self.JudulCreate()
        self.addTags()
        print(self.nama_file)
        print(self.tags)
        
        self.generateTemplate()

p = MainAutoGenerateTemplate()
p.main()