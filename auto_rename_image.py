import shutil
import json
import os
os.system('cls')


'''
Pengambilan data
'''
full_path = os.getcwd()
path_post = os.path.join(full_path, '_posts')
path_gambar = os.path.join(full_path, 'assets', 'images')


list_posts = os.listdir(path_post)
list_gambar = os.listdir(path_gambar)

database = {}
for post in list_posts:
    name = post.split('-', maxsplit=3)[-1]
    name = name.replace('.md', '')
    
    path = os.path.join(path_post, post)
    if os.path.isdir(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        daftar_img = [d.replace('\n', '') for d in data if '(../assets/images' in d]
        database[name] = daftar_img

#print(json.dumps(database, indent=4))

'''
Pembuatan Dir untuk setiap Postingan
'''
for data in database.keys():
    path_make_post = os.path.join(path_gambar, data)
    # jika dir sesuai nama post tidak ada, akan buat baru
    if os.path.exists(path_make_post) != True:
        os.mkdir(path_make_post)

def move_gambar():
    '''
    Pemindahan Gambar Sesuai Postingan
    '''
    for data in database.keys():
        path_make_post = os.path.join(path_gambar, data)
        for gambar in database[data]:
            print(gambar)
            name = gambar[:-1].split('/')[-1]
            print(gambar)
            path_gambar_asli = os.path.join(path_gambar, name)
            path_gambar_baru = os.path.join(path_make_post, name)

            print(os.path.exists(path_gambar_asli))
            # jika gambar baru belum ada, maka copy gambar
            if os.path.exists(path_gambar_baru) != True:
                shutil.copy(path_gambar_asli, path_make_post)

def update_lokasi_gambar_blog():
    '''
    Update lokasi file gambar untuk blog nya
    '''
    for post in list_posts:
        template = '![Branching](../assets/images/{}{})'

        name = post.split('-', maxsplit=3)[-1]
        name = name.replace('.md', '')
        if database[name] == []: continue
        path = os.path.join(path_post, post)
        with open(path, 'r+', encoding='utf-8') as f:
            content_data = f.read()
            for replacement in database[name]:
                name_file = replacement[:-1].split('/')[-1]
                content_data = content_data.replace(
                    replacement,
                    template.format(name, '/'+name_file)
                )
                f.seek(0)
                f.write(content_data)
                f.truncate()

def main():
    pass

if __name__ == '__main__':
    main()