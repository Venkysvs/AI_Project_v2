from core.clarifier import needs_clarification, QUESTIONS

class Conversation:
    def __init__(self):
        self.intent = None
        self.service = None
        self.pending_params = {}
        self.current_field = None

    def start_request(self, intent, service, params):
        self.intent = intent
        self.service = service

        # ✅ Normalize keys
        normalized = {}
        for k, v in params.items():
            if k.lower() == "region":
                normalized["Region"] = v
            elif k.lower() == "provider":
                normalized["Provider"] = v
            elif k.lower() == "instancetype":
                normalized["InstanceType"] = v
            elif k.lower() == "os":
                normalized["OS"] = v
            elif k.lower() == "subnetid":
                normalized["SubnetId"] = v
            elif k.lower() == "securitygroupid":
                normalized["SecurityGroupId"] = v
            elif k.lower() == "keyname":
                normalized["KeyName"] = v
            elif k.lower() == "name":
                normalized["Name"] = v
            elif k.lower() == "instanceid":
                normalized["InstanceId"] = v
            else:
                normalized[k] = v

        # ✅ Default region fallback
        if "Region" not in normalized:
            normalized["Region"] = "us-east-1"

        self.pending_params = normalized
        return self.next_question()

    def next_question(self):
        """Ask next missing parameter"""
        field = needs_clarification(self.service, self.pending_params, self.intent)
        if not field:
            return None  # ready to dispatch
        self.current_field = field
        return QUESTIONS[field]

    def record_answer(self, answer):
        """Record user answer and continue"""
        if self.current_field:
            self.pending_params[self.current_field] = answer
        return self.next_question()

    def is_ready(self):
        """Check if all required fields are filled"""
        return needs_clarification(self.service, self.pending_params, self.intent) is None

# ✅ alias for backward compatibility
ConversationManager = Conversation
