
import os, sys
import gradio as gr
from src.gradio_demo import SadTalker  

try:
    import webui
    in_webui = True
except:
    in_webui = False


def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 🎬 数字人说话视频生成器 </h2>                     <p style='font-size:16px;color: #888'>上传人像照片 + 文字/克隆声音 → 自动生成口型对齐的说话视频</p> </div>")
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('📷 上传人像照片'):
                        source_image = gr.Image(label="人像照片（正面、光线均匀）", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('🎤 语音/文字转语音'):
                        driven_audio = gr.Audio(label="驱动音频", source="upload", type="filepath")
                        if sys.platform != 'win32' and not in_webui: 
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="输入文字（将转为语音）", lines=5, placeholder="请输入要合成的文字内容...")
                                ref_audio = gr.Audio(label="参考音频（克隆声音）", source="upload", type="filepath")
                                tts = gr.Button('🔊 生成语音', elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text, ref_audio], outputs=[driven_audio])
                            
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('⚙️ 生成设置'):
                        with gr.Column(variant='panel'):
                            preprocess_type = gr.Radio(['full', 'crop', 'resize'], value='full', label='图片预处理')
                            is_still_mode = gr.Checkbox(label="静止模式（减少头部摆动）", value=False)
                            enhancer = gr.Checkbox(label="人脸增强（GFP-GAN）", value=True)
                            batch_size = gr.Slider(label="生成批量大小", step=1, maximum=10, value=1)
                            size_of_image = gr.Radio([256], value=256, label='人脸模型分辨率')
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="头部姿态风格（0最自然）", value=0)
                            submit = gr.Button('🎬 生成视频', elem_id="sadtalker_generate", variant='primary')
                            
                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="生成的视频", format="mp4").style(width=256)

        submit.click(
                    fn=sad_talker.test, 
                    inputs=[source_image,
                            driven_audio,
                            preprocess_type,
                            is_still_mode,
                            enhancer,
                            batch_size,                            
                            size_of_image,
                            pose_style
                            ], 
                    outputs=[gen_video]
                    )

    return sadtalker_interface
 

if __name__ == "__main__":
    demo = sadtalker_demo()
    demo.queue()
    demo.launch(server_name="0.0.0.0", server_port=7860)
