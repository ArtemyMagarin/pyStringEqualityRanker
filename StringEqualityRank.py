class StringEqualityRank:
    def __init__(self, 
                string1, 
                string2, 
                THRESHOLD_SENTENCE = 0.25,
                THRESHOLD_WORD     = 0.45,
                MIN_WORD_LENGTH    = 3,
                SUBTOKEN_LENGTH    = 2):

        self.string1 = string1
        self.string2 = string2
        
        self.THRESHOLD_SENTENCE = THRESHOLD_SENTENCE
        self.THRESHOLD_WORD     = THRESHOLD_WORD
        self.MIN_WORD_LENGTH    = MIN_WORD_LENGTH
        self.SUBTOKEN_LENGTH    = SUBTOKEN_LENGTH


    def normalize_string(self, s):
        return ''.join(list(filter(lambda x: (x.isalnum() or x==' '), list(s)))).lower()


    def get_tokens(self, s):
        return list(filter(lambda x: len(x) >= self.MIN_WORD_LENGTH, s.split(' ')))


    def is_tokens_fuzzy_equal(self, firstToken, secondToken):

        equalSubtokensCount = 0;
        usedTokens = []

        for i in range(len(firstToken) - self.SUBTOKEN_LENGTH + 1):
            subtokenFirst = firstToken[i:i+self.SUBTOKEN_LENGTH]

            for j in range(len(secondToken) - self.SUBTOKEN_LENGTH + 1):
                subtokenSecond = secondToken[j:j+self.SUBTOKEN_LENGTH]

                if subtokenSecond not in usedTokens and subtokenFirst == subtokenSecond:
                    equalSubtokensCount += 1
                    usedTokens.append(subtokenSecond)

        

        subtokenFirstCount  = len(firstToken)  - self.SUBTOKEN_LENGTH + 1;
        subtokenSecondCount = len(secondToken) - self.SUBTOKEN_LENGTH + 1;

        tanimoto = (1.0 * equalSubtokensCount) / (subtokenFirstCount + subtokenSecondCount - equalSubtokensCount);

        return self.THRESHOLD_WORD <= tanimoto; 


    def get_fuzzy_equals_tokens(self, firstTokens, secondTokens):
        usedTokens = []
        equalsTokens = []

        for f_token in firstTokens:
            for s_token in secondTokens:
                if s_token not in usedTokens and self.is_tokens_fuzzy_equal(f_token, s_token):
                    equalsTokens.append(f_token)
                    usedTokens.append(s_token)

        return equalsTokens



    def get_coef(self):
        t1 = self.get_tokens(self.normalize_string(self.string1))
        t2 = self.get_tokens(self.normalize_string(self.string2))

        equalsTokens = self.get_fuzzy_equals_tokens(t1, t2)

        return len(equalsTokens) / (len(t1) + len(t2) - len(equalsTokens))
