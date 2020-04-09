# English Vesrion
This is an revised version from [SynthText](https://github.com/ankush-me/SynthText/) and [Chinese SynthText](https://github.com/JarveeLee/SynthText_Chinese_version), which is more suitable to generate customized data, e.g. generating multiple data same as the text data in game. It works for both Chinese and English.

## Modify 
* Add function to customize the font size, color
* Add UI interface , which is more easier for fresh user
* Delete character augmentation, e.g. no border, no shadow 


## Enviroment
* python3, Windows,Ubuntu

## Run app
`python GUIstart.py`

## Usage Steps 
### Step 1: Prepare background image  
Click `open data path` button, Choose a folder and confirm,the image number under the chosen folder will be popped up as the picture shows   
 
<img src="./util/source/step1.png"  height = "200" />

### Step 2: Select font style by two ways
 1. The first way is to select from the `combobox` which is provided by current tool;
 2. The second way is to click `add font` button and choose the font file  what users want.  
 The chosen font will be listed in `fontlist`. You can clear all the fonts by clicking `clear` button. Deleting one specific font is not supported so far.
<img src="./util/source/step2.png" height = "200"  />

### Step 3: Input the character property what you want.   
Here is the example for character “WINNER WINNER CHICKEN DINNER”. 
* Input `40` for the font size 
* Choose color by clicking `open color palette` button
* Input `1` for the reusing number for each image
* Input `1` for the text number in each image
* Set the text content by clicking `import text source` button with a `txt` file or entering text directly in the box area.  

<img src="./util/source/step3.png" height = "200"  />

### Step 4: Generate data 
Click the button `generate data` , `generate detection label` and `generate recognition label` step by step, it will show the messages as the pictures show.  

<img src="./util/source/step4.png"  height = "200"  /> 

* detection label format
```
222,230,601,230,601,271,222,271,WINNER WINNER CHICKEN DINNER

#value oder
(left,top) ---> (right,top)
                    |
                    |
                    v
(left,bottom) <--- (right,bottom)
```
* recognition label format
```
test3_000_000.png WINNER WINNER CHICKEN DINNER
```

## Visualization
Here is the example after `Usage Steps`   

<img src="./util/source/test3_vis.png" width = "400" height = "250" /> 


# 中文
这是基于[SynthText](https://github.com/ankush-me/SynthText/)和[Chinese SynthText](https://github.com/JarveeLee/SynthText_Chinese_version)进行修改的项目，适用于生成自定义数据，如生成大量跟游戏文字相同的数据。 它适用于中文和英文。

## 主要修改
* 生成定制化文本数据，指定字体大小、颜色等
* 增加UI交互，方便操作
* 删除字体增强功能，没有对字体渲染阴影，边框等

## 环境
* python3, Windows,Ubuntu

## 运行程序
`python GUIstart.py`

## 使用步骤
### 步骤一: 准备背景图片 
按 `open data path` 按键, 选择一个文件并且确定，所选文件夹下的图像编号将作为图片弹出   
 
<img src="./util/source/step1.png"  height = "200" />

### 步骤二: 选择格式的了两种方法
 1. 第一种方法是在复选框种选择想要的格式，选完后点击`comfirm`按钮确认;
 2. 第二种方法是点击`add font`按钮，选择想要的格式。
 被选择的格式会添加在右边的列表中，可以用`clear`按钮来清除所有，暂时不支持清楚单个格式
<img src="./util/source/step2.png" height = "200"  />

### 步骤三: 输入想要的文本
这里有个文本样式作为参考　文本内容：“大吉大利，今晚吃鸡”
参数解析：
* fontsize:文本大小
* fontcolor:文本颜色、
* reusing number for each image：每张图片复用次数
* text number in each image：每张图片中的文本数量
* text content：文本内容

* 输入 `35` 在 `font size`输入框中 
* 点击按钮 `open color palette` 来选择颜文本色
* 输入`1` 在 `reusing number for each image`输入框中
* 输入`1` 在`for the text number in each image`输入框中
* 点击按钮 `import text source` 来设置文本内容，可以选择`txt`文件或者根据提示自定义文本内容在输入框中 

<img src="./util/source/step3.png" height = "200"  />

### 步骤四: 生成数据 
依次按下按钮 `generate data` , `generate detection label` 和　`generate recognition label` , 按完后会弹窗显示生成的本文信息 

<img src="./util/source/step4.png"  height = "200"  /> 

* 文本检测标签的格式
```
222,230,601,230,601,271,222,271,WINNER WINNER CHICKEN DINNER

#坐标点顺序
(左边,顶部) ---> (右边,顶部)
                    |
                    |
                    v
(左边,底部) <--- (右边,底部)
```
* 识别标签的格式
```
test3_000_000.png WINNER WINNER CHICKEN DINNER
```

## 可视化
<img src="./util/source/test2_vis.png" width = "400" height = "250"/> 






