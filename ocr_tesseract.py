import pyocr
from PIL import Image, ImageEnhance
import os

# Path設定
TESSERACT_PATH = "/Users/nagashimadaichi/Work/AI_experience/tessdata" #インストールしたTesseract-OCRのpath
TESSDATA_PATH = "/Users/nagashimadaichi/Work/AI_experience/tesseract/tessdata" #tessdataのpath

IMG_PATH = "/Users/nagashimadaichi/Work/AI_experience/採血結果_demo.jpg" #解析画像のpath

os.environ["PATH"] += os.pathsep + TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

# OCRエンジン取得
tools = pyocr.get_available_tools()
tool = tools[0]

# OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

# 画像読み込み
img = Image.open(IMG_PATH) #他の拡張子でもOK

# 画像処理
img_g = img.convert('L') #Gray変換
enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
img_con = enhancer.enhance(2.0) #コントラストを上げる

# 画像からOCRで日本語を読んで、文字列として取り出す
img_con.save("/Users/nagashimadaichi/Work/AI_experience/enchanced.jpg")
txt_pyocr = tool.image_to_string(img_con, lang='jpn', builder=builder)

# 半角スペースを消す
txt_pyocr = txt_pyocr.replace(' ', '')

print(txt_pyocr)