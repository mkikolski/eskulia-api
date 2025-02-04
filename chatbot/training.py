# from unsloth import FastLanguageModel
# import torch
#
# model, tokenizer = FastLanguageModel.from_pretrained(
#     model_name = "unsloth/llama-3-8b-bnb-4bit",
#     max_seq_length = 1024,
#     dtype = None,
#     load_in_4bit = True,
# )
#
# model = FastLanguageModel.get_peft_model(
#     model,
#     r = 16,
#     target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
#     lora_alpha = 16,
#     lora_dropout = 0,
#     bias = "none",
#     use_gradient_checkpointing = True,
#     random_state = 3407,
#     use_rslora = False,
#     loftq_config = None,
# )
#
# # Dodać model treningu
#
# FastLanguageModel.for_inference(model)
# inputs = tokenizer([
#     f"""You're an expert in pharmacy. Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
#
#     ### Instruction:
#     {"Provide information on given drug"}
#
#     ### Input:
#     {"Paxtin"}
#
#     ### Response:
#     """
# ], return_tensors = "pt").to("cuda")
#
# outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
# tokenizer.batch_decode(outputs)