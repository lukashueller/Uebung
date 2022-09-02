import torch

from transformers import BertTokenizer, BertForMaskedLM

# inspired by https://github.com/renatoviolin/next_word_prediction

class BERT:
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased')
    bert_model = BertForMaskedLM.from_pretrained('bert-base-german-cased').eval()

    @staticmethod
    def decode(tokenizer, pred_idx, top_clean):
        tokens = []
        for w in pred_idx:
            token = ''.join(tokenizer.ids_to_tokens[w].split()) #TODO: change to decode
            if token not in ["[PAD]", "[UNK]"] and "unused_punctuation" not in token:
                tokens.append(" " + token if not token.startswith("##") else token.replace("##", ""))
        return tokens[:top_clean]


    @staticmethod
    def encode(tokenizer, text_sentence, add_special_tokens=True):
        text_sentence = text_sentence.replace("<mask>", tokenizer.mask_token)
        # if <mask> is the last token, append a "." so that models dont predict punctuation.
        text_sentence += ' .'

        input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
        mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
        return input_ids, mask_idx

    def get_bert_predictions(self, text_sentence, top_clean=10):
        input_ids, mask_idx = self.encode(self.bert_tokenizer, text_sentence + " <mask>")
        with torch.no_grad():
            predict = self.bert_model(input_ids)[0]
        return self.decode(self.bert_tokenizer, predict[0, mask_idx, :].topk(top_clean*2+10).indices.tolist(), top_clean)
