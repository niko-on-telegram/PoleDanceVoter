import json
import logging
from pathlib import Path
import shutil

i = -1
video_names = ['presentation.mp4', 'video_cut.mp4', 'video_uncut.mp4']
photo_i = 0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: " "%(filename)s: " "%(levelname)s: " "%(funcName)s(): " "%(lineno)d:\t" "%(message)s",
)


def suggest_filename(name: str) -> str:
    name = name.lower()
    if name.startswith('img_') and name.endswith('.png'):
        counter4img = name[4:8]
        counter4img = int(counter4img)
        if 7000 < counter4img < 7200:
            return 'afisha.PNG'
    if name.endswith('.mp4') or name.endswith('.mov'):
        global i
        i += 1
        i %= 3
        return video_names[i]
    global photo_i
    if name.endswith('.jpg') or name.endswith('.jpeg'):
        photo_i += 1
        return f"photo{photo_i}.jpg"
    if name.endswith('.heic'):
        photo_i += 1
        return f"photo{photo_i}.heic"
    if name.endswith('.png'):
        photo_i += 1
        return f"photo{photo_i}.png"
    assert False, name


pt = "/home/gridgain/Downloads/Telegram Desktop/ChatExport_2024-10-20/result.json"
base_path = "/home/gridgain/Downloads/Telegram Desktop/ChatExport_2024-10-20"
target_dir = "/home/gridgain/PycharmProjects/PoleDanceVoter/data/competitors_data"

with open(pt) as f:
    data = json.load(f)
msgs = data['messages'][14:]
group_by_cont = {}
single_cont = []
from_saved = None
counter = 0
for msg in msgs:
    fn = msg.get('file_name', None)
    if fn and fn.startswith('IMG_') and fn.endswith('.PNG'):
        counter_img = fn[4:8]
        counter_img = int(counter_img)
        if 7000 < counter_img < 7200:
            group_by_cont[counter] = {'files': single_cont, 'user': from_saved}
            single_cont = []
            from_saved = None
            counter += 1
    file = msg.get('file', None)
    if file:
        single_cont.append(file)
    photo = msg.get('photo', None)
    if photo:
        single_cont.append(photo)
    from_user = msg.get('forwarded_from', None)
    if from_saved is None and from_user:
        from_saved = from_user
    assert any([file, photo, msg.get('text', None)])

group_by_cont[counter] = {'files': single_cont, 'user': from_saved}
del group_by_cont[0]
pass

for item in group_by_cont.values():
    dst = Path(target_dir) / item['user']
    if dst.exists():
        continue
    dst.mkdir()
    for file in item['files']:
        src_file = Path(base_path) / file
        if src_file.name.startswith('безым'):
            logging.info(f"Skipping {src_file=}")
            continue
        if src_file.name.endswith('.ogg'):
            logging.info(f"Skipping {src_file}")
            continue
        dst_filename = suggest_filename(src_file.name)

        dst_file = dst / dst_filename
        print(f"Copying from {src_file=} to {dst_file=}")
        assert not dst_file.exists()
        shutil.copy(src_file, dst_file)
