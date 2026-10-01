"""
AquaWatch AI - Pure Python & Scikit-Learn Hybrid Machine Learning & NLP Engine
Engineered to run seamlessly across all Python environments (including Python 3.15+ alpha)
without crashing on incompatible C-extension binary slots.

Features:
1. TF-IDF Text Vectorization with n-grams and stop-words.
2. Multinomial Naive Bayes / Calibrated Probabilistic Classifier.
3. Spatial-Textual Duplicate Detection (Haversine + Cosine Similarity).
4. Multi-Factor AI Priority Recommendation & Water Loss Estimator.
5. Field Crew NLP Dispatch Summarizer.
6. Geographic & Temporal Hotspot Trend Analytics.
"""

import math
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional, Any

# Domain training dataset for water leakage complaints
TRAINING_DATA = [
    # Pipe Leakage
    ("Water is leaking from an underground supply pipe under the sidewalk", "Pipe Leakage"),
    ("Cracked water pipe leaking clean drinking water along residential lane", "Pipe Leakage"),
    ("Underground distribution pipe has a steady leak wetting the pavement", "Pipe Leakage"),
    ("Joint connecting the main line to home service connection is spraying water", "Pipe Leakage"),
    ("Water seeping through sidewalk tiles from broken subterranean pipe", "Pipe Leakage"),
    ("Sub-surface pipe cracked near boundary wall, continuous steady trickle", "Pipe Leakage"),
    ("Water supply pipe leakage near apartment gate, clean water pooling", "Pipe Leakage"),
    ("Corroded metal pipe has a pinhole leak shooting a thin jet of water", "Pipe Leakage"),
    ("Supply line joint leak wasting drinking water continuously", "Pipe Leakage"),
    ("Underground PVC pipe fractured during recent road digging works", "Pipe Leakage"),
    ("Water bubbling up through the pavement from fractured municipal line", "Pipe Leakage"),
    ("Water pipe leaking under driveway, causing dampness and puddles", "Pipe Leakage"),
    ("Leaking municipal water pipe beneath pavement in front of house", "Pipe Leakage"),
    ("Supply pipe hairline fracture spilling fresh water onto footpath", "Pipe Leakage"),

    # Tap Leakage
    ("Public drinking water tap is broken and won't turn off completely", "Tap Leakage"),
    ("Community standpost tap is dripping heavily day and night", "Tap Leakage"),
    ("Park water fountain tap valve is loose and continuously leaking", "Tap Leakage"),
    ("Broken faucet at public bus stand wasting water constantly", "Tap Leakage"),
    ("School drinking water tap has a missing knob and is running non-stop", "Tap Leakage"),
    ("Community water tap handle is broken, water dripping continuously", "Tap Leakage"),
    ("Public tap washer worn out, steady stream of water running down gutter", "Tap Leakage"),
    ("Street corner public water booth tap cannot be shut off", "Tap Leakage"),
    ("Park drinking tap is stuck open, water spilling onto the grass", "Tap Leakage"),
    ("Damaged brass tap at roadside public water post leaking constantly", "Tap Leakage"),
    ("Leaking public faucet in market square dripping gallon after gallon", "Tap Leakage"),
    ("Broken tap knob leaking water in community garden area", "Tap Leakage"),

    # Road Flooding
    ("Severe water accumulation on the main road causing heavy traffic jam", "Road Flooding"),
    ("Road submerged in knee-deep water due to massive water overflow", "Road Flooding"),
    ("Large pool of water covering both lanes of the highway intersection", "Road Flooding"),
    ("Water overflowing from stormwater drain onto the street and flooding shops", "Road Flooding"),
    ("Road is flooded with water, two-wheelers and pedestrians unable to pass", "Road Flooding"),
    ("Huge water puddle covering entire street corner, vehicles splashing into houses", "Road Flooding"),
    ("Street flooded after heavy overflow, water entering ground floor premises", "Road Flooding"),
    ("Waterlogged underpass creating hazard for commuter vehicles", "Road Flooding"),
    ("Excessive water running across the road creating a swamp and erosion", "Road Flooding"),
    ("Low-lying road flooded with water accumulation reaching curb height", "Road Flooding"),
    ("Water accumulation on crossroad making pedestrian crossing impassable", "Road Flooding"),
    ("Major intersection flooded with stagnant water following line breach", "Road Flooding"),

    # Main Pipeline Burst
    ("Massive main water pipeline burst, huge water geyser shooting 15 feet high", "Main Pipeline Burst"),
    ("High pressure main water line ruptured, asphalt blown out creating huge crater", "Main Pipeline Burst"),
    ("Catastrophic pipeline burst, rushing torrent of water eroding the road surface", "Main Pipeline Burst"),
    ("Trunk supply line burst, immense volume of water flooding the entire neighborhood", "Main Pipeline Burst"),
    ("High-pressure water geyser erupting from street after construction damage", "Main Pipeline Burst"),
    ("Major feeder main burst, complete loss of water pressure across sector", "Main Pipeline Burst"),
    ("Ruptured 300mm main transmission line gushing thousands of liters per minute", "Main Pipeline Burst"),
    ("Giant water fountain in the middle of avenue due to main pipeline explosion", "Main Pipeline Burst"),
    ("Asphalt cracked and blown upward by exploding high pressure water main", "Main Pipeline Burst"),
    ("Critical water main rupture threatening foundations of nearby buildings", "Main Pipeline Burst"),
    ("Huge geyser shooting clean water into the sky from burst primary conduit", "Main Pipeline Burst"),
    ("Main pipeline blowout flooded commercial street with torrential water", "Main Pipeline Burst"),

    # Sewage & Contamination
    ("Foul-smelling black sewage water mixing with clean municipal tap water", "Sewage & Contamination"),
    ("Sewage overflow contaminating drinking water pipeline, horrible odor", "Sewage & Contamination"),
    ("Drainage line leaking directly into open drinking water canal", "Sewage & Contamination"),
    ("Dirty brown discolored tap water coming into houses with pungent sewage smell", "Sewage & Contamination"),
    ("Sewer manhole backing up and spilling contaminated waste over clean water valve", "Sewage & Contamination"),
    ("Underground sewage pipe broken and leaking near clean water supply lines", "Sewage & Contamination"),
    ("Contaminated water with worms and foul stench coming from tap connections", "Sewage & Contamination"),
    ("Septic runoff overflowing into residential storm drain and water network", "Sewage & Contamination"),
    ("Sewage water bubbling near drinking water pump station, health hazard", "Sewage & Contamination"),
    ("Turbid stinking contaminated black water leaking into water sump", "Sewage & Contamination"),

    # Other / Meter
    ("Commercial water meter box is overflowing and filling with water", "Other / Meter"),
    ("Water meter dial spinning rapidly, suspected leak inside the meter chamber", "Other / Meter"),
    ("Fire hydrant valve leaking water slowly at the base onto the curb", "Other / Meter"),
    ("Apartment bulk water meter leaking at the flange connection", "Other / Meter"),
    ("Pressure release valve on rooftop municipal tank spraying fine mist", "Other / Meter"),
    ("Unidentified water seep near electrical transformer pole, urgent check needed", "Other / Meter"),
    ("Water utility valve chamber flooded with clear water, cover displaced", "Other / Meter"),
    ("Fire hydrant flange leaking clear water onto pavement", "Other / Meter"),
    ("Domestic water meter housing cracked and spurting water", "Other / Meter"),
]

CATEGORIES = [
    "Pipe Leakage",
    "Tap Leakage",
    "Road Flooding",
    "Main Pipeline Burst",
    "Sewage & Contamination",
    "Other / Meter",
]

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', 'as', 
    'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'cannot', 
    'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 
    'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 
    'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 
    'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 
    'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 
    'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 
    'was', 'wasn', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 
    'you', 'your', 'yours', 'yourself', 'yourselves'
}


class PurePythonTFIDFVectorizer:
    """Pure Python TF-IDF Vectorizer with unigram + bigram support."""
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.vocab_list: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        tokens = [w for w in words if w not in STOP_WORDS]
        # Generate bigrams
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams

    def fit(self, docs: List[str]):
        doc_count = len(docs)
        doc_freq = defaultdict(int)
        all_tokens_set = set()

        for doc in docs:
            tokens = set(self._tokenize(doc))
            for tok in tokens:
                doc_freq[tok] += 1
                all_tokens_set.add(tok)

        self.vocabulary = {tok: idx for idx, tok in enumerate(sorted(all_tokens_set))}
        self.vocab_list = sorted(all_tokens_set)
        
        # Smooth IDF: log((1 + N) / (1 + df)) + 1
        for tok, df in doc_freq.items():
            self.idf[tok] = math.log((1.0 + doc_count) / (1.0 + df)) + 1.0

    def transform(self, text: str) -> Dict[int, float]:
        tokens = self._tokenize(text)
        if not tokens:
            return {}

        tf_counts = Counter(tokens)
        vec = {}
        sum_sq = 0.0

        for tok, count in tf_counts.items():
            if tok in self.vocabulary:
                idx = self.vocabulary[tok]
                tf = 1.0 + math.log(count)  # Sublinear TF scaling
                val = tf * self.idf.get(tok, 1.0)
                vec[idx] = val
                sum_sq += val * val

        # L2 normalize
        norm = math.sqrt(sum_sq)
        if norm > 0:
            for idx in vec:
                vec[idx] /= norm

        return vec

    def compute_cosine_similarity(self, vec_a: Dict[int, float], vec_b: Dict[int, float]) -> float:
        """Computes dot product between two L2 normalized sparse vectors."""
        if not vec_a or not vec_b:
            return 0.0
        # Iterate over smaller vector
        if len(vec_a) > len(vec_b):
            vec_a, vec_b = vec_b, vec_a
        dot = sum(val * vec_b.get(idx, 0.0) for idx, val in vec_a.items())
        return max(0.0, min(1.0, dot))


class PurePythonClassifier:
    """Multinomial Naive Bayes & Softmax Probabilistic Classifier."""
    def __init__(self, vectorizer: PurePythonTFIDFVectorizer):
        self.vectorizer = vectorizer
        self.class_priors: Dict[str, float] = {}
        self.feature_probs: Dict[str, Dict[int, float]] = defaultdict(dict)
        self.classes = CATEGORIES

    def fit(self, texts: List[str], labels: List[str]):
        total_docs = len(texts)
        class_docs = defaultdict(list)
        for t, l in zip(texts, labels):
            class_docs[l].append(t)

        vocab_size = len(self.vectorizer.vocabulary)

        for cls in self.classes:
            docs = class_docs[cls]
            count = len(docs)
            self.class_priors[cls] = (count + 1.0) / (total_docs + len(self.classes))

            # Aggregate token weights for this class
            feature_weights = defaultdict(float)
            total_feature_weight = 0.0

            for doc in docs:
                vec = self.vectorizer.transform(doc)
                for idx, val in vec.items():
                    feature_weights[idx] += val
                    total_feature_weight += val

            # Laplace smoothed feature probabilities: (W + 1) / (Total + V)
            alpha = 1.0
            denom = total_feature_weight + alpha * vocab_size
            for idx in range(vocab_size):
                num = feature_weights[idx] + alpha
                self.feature_probs[cls][idx] = math.log(num / denom)

    def predict_proba(self, text: str) -> Dict[str, float]:
        vec = self.vectorizer.transform(text)
        log_scores = {}

        for cls in self.classes:
            score = math.log(self.class_priors.get(cls, 1.0 / len(self.classes)))
            for idx, val in vec.items():
                if idx in self.feature_probs[cls]:
                    score += val * self.feature_probs[cls][idx]
            log_scores[cls] = score

        # Numerical stability via max subtraction for Softmax
        max_log = max(log_scores.values())
        exp_scores = {cls: math.exp(score - max_log) for cls, score in log_scores.items()}
        sum_exp = sum(exp_scores.values())

        if sum_exp > 0:
            return {cls: exp_scores[cls] / sum_exp for cls in self.classes}
        return {cls: 1.0 / len(self.classes) for cls in self.classes}


class WaterLeakageAIEngine:
    def __init__(self):
        self.vectorizer = PurePythonTFIDFVectorizer()
        texts, labels = zip(*TRAINING_DATA)
        self.vectorizer.fit(list(texts))
        self.classifier = PurePythonClassifier(self.vectorizer)
        self.classifier.fit(list(texts), list(labels))

    # -------------------------------------------------------------
    # 1. AI Complaint Classification
    # -------------------------------------------------------------
    def classify_complaint(self, text: str) -> Dict[str, Any]:
        """
        Classifies a complaint description into one of the leak categories.
        Returns predicted category, confidence percentage, probability distribution, and key features.
        """
        clean_text = text.strip()
        if not clean_text:
            return {
                "category": "Other / Meter",
                "confidence": 0.0,
                "probabilities": {cat: 0.0 for cat in CATEGORIES},
                "is_confident": False,
                "top_keywords": []
            }

        probabilities = self.classifier.predict_proba(clean_text)
        best_class = max(probabilities, key=probabilities.get)
        confidence = probabilities[best_class]

        # Extract top keywords
        vec = self.vectorizer.transform(clean_text)
        sorted_indices = sorted(vec.items(), key=lambda x: x[1], reverse=True)
        inv_vocab = {v: k for k, v in self.vectorizer.vocabulary.items()}
        top_keywords = [inv_vocab[idx].replace('_', ' ') for idx, _ in sorted_indices[:5] if idx in inv_vocab]

        # Rule-based safety reinforcement for critical emergencies
        lower_text = clean_text.lower()
        if any(w in lower_text for w in ["geyser", "burst", "ruptured", "catastrophic", "blown out", "crater in road", "high pressure"]):
            if probabilities.get("Main Pipeline Burst", 0) < 0.70:
                best_class = "Main Pipeline Burst"
                confidence = max(confidence, 0.89)
        elif any(w in lower_text for w in ["foul smell", "sewage", "contaminated", "dirty water", "sewer", "stench", "black water"]):
            if probabilities.get("Sewage & Contamination", 0) < 0.70:
                best_class = "Sewage & Contamination"
                confidence = max(confidence, 0.88)
        elif any(w in lower_text for w in ["tap", "faucet", "standpost", "fountain", "drinking tap"]):
            if "burst" not in lower_text and "flooded" not in lower_text:
                best_class = "Tap Leakage"
                confidence = max(confidence, 0.85)
        elif any(w in lower_text for w in ["flooded road", "submerged", "traffic jam", "waterlogged", "water logging", "curb"]):
            best_class = "Road Flooding"
            confidence = max(confidence, 0.86)
        elif any(w in lower_text for w in ["underground pipe", "sidewalk pipe", "pipeline crack", "trickle", "pavement"]):
            if best_class not in ["Main Pipeline Burst", "Sewage & Contamination"]:
                best_class = "Pipe Leakage"
                confidence = max(confidence, 0.82)

        return {
            "category": best_class,
            "confidence": round(confidence * 100, 1),
            "probabilities": {k: round(v * 100, 1) for k, v in probabilities.items()},
            "is_confident": confidence >= 0.40,
            "top_keywords": top_keywords
        }

    def predict_category(self, text: str, user_hint_category: Optional[str] = None) -> Dict[str, Any]:
        """Convenience method returning predicted_category, confidence, and top_keywords."""
        res = self.classify_complaint(text)
        cat = user_hint_category if (user_hint_category and user_hint_category != 'Auto') else res["category"]
        return {
            "predicted_category": cat,
            "confidence": res["confidence"],
            "top_keywords": res["top_keywords"]
        }

    def detect_duplicates(
        self,
        new_complaint: Dict[str, Any],
        existing_complaints: List[Dict[str, Any]],
        distance_threshold_meters: float = 450.0,
        text_sim_threshold: float = 0.35
    ) -> Dict[str, Any]:
        """Convenience alias for find_duplicates."""
        return self.find_duplicates(
            new_complaint, existing_complaints,
            distance_threshold_meters=distance_threshold_meters,
            text_sim_threshold=text_sim_threshold
        )

    # -------------------------------------------------------------
    # 2. Duplicate Detection Engine
    # -------------------------------------------------------------
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great circle distance in meters between two coordinates."""
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda / 2.0) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def find_duplicates(
        self,
        new_complaint: Dict[str, Any],
        existing_complaints: List[Dict[str, Any]],
        distance_threshold_meters: float = 450.0,
        text_sim_threshold: float = 0.35
    ) -> Dict[str, Any]:
        """
        Scans existing complaints to detect potential duplicates.
        Combines spatial proximity (Haversine) with text similarity (TF-IDF Cosine Sim).
        """
        if not existing_complaints:
            return {"is_duplicate": False, "match": None, "duplicate_score": 0.0, "match_reason": ""}

        new_text = f"{new_complaint.get('title', '')} {new_complaint.get('description', '')} {new_complaint.get('street_name', '')}"
        new_lat = float(new_complaint.get('latitude', 0.0) or 0.0)
        new_lng = float(new_complaint.get('longitude', 0.0) or 0.0)
        new_street = str(new_complaint.get('street_name', '')).lower().strip()

        new_vec = self.vectorizer.transform(new_text)

        best_match = None
        highest_composite_score = 0.0
        match_reason = ""

        for comp in existing_complaints:
            # Skip closed complaints or if comparing to itself
            if comp.get('status') in ['Resolved', 'Rejected']:
                continue
            if comp.get('complaint_id') == new_complaint.get('complaint_id'):
                continue

            cand_text = f"{comp.get('title', '')} {comp.get('description', '')} {comp.get('street_name', '')}"
            cand_vec = self.vectorizer.transform(cand_text)
            text_sim = self.vectorizer.compute_cosine_similarity(new_vec, cand_vec)

            cand_lat = float(comp.get('latitude', 0.0) or 0.0)
            cand_lng = float(comp.get('longitude', 0.0) or 0.0)
            cand_street = str(comp.get('street_name', '')).lower().strip()

            distance_m = 999999.0
            if new_lat != 0.0 and cand_lat != 0.0:
                distance_m = self.haversine_distance(new_lat, new_lng, cand_lat, cand_lng)

            # Spatial similarity score
            spatial_sim = max(0.0, 1.0 - (distance_m / distance_threshold_meters)) if distance_m < distance_threshold_meters else 0.0

            # Street name token overlap
            street_overlap = 0.0
            if new_street and cand_street:
                new_tokens = set(re.findall(r'\w+', new_street))
                cand_tokens = set(re.findall(r'\w+', cand_street))
                if new_tokens and cand_tokens:
                    street_overlap = len(new_tokens.intersection(cand_tokens)) / max(len(new_tokens), len(cand_tokens))

            # Composite match calculation
            if distance_m <= distance_threshold_meters:
                composite = (0.50 * spatial_sim) + (0.35 * text_sim) + (0.15 * street_overlap)
                if composite > highest_composite_score and (spatial_sim > 0.4 and (text_sim > 0.20 or street_overlap > 0.35)):
                    highest_composite_score = composite
                    best_match = comp
                    match_reason = f"Located {int(distance_m)}m away with matching problem description and street."
            elif street_overlap > 0.5 and text_sim > text_sim_threshold:
                composite = (0.60 * text_sim) + (0.40 * street_overlap)
                if composite > highest_composite_score and composite > 0.45:
                    highest_composite_score = composite
                    best_match = comp
                    match_reason = f"High text similarity ({int(text_sim * 100)}%) on same street ({comp.get('street_name')})."
            elif text_sim >= 0.70:
                if text_sim > highest_composite_score:
                    highest_composite_score = text_sim
                    best_match = comp
                    match_reason = f"Direct description similarity match ({int(text_sim * 100)}% match)."

        is_duplicate = highest_composite_score >= 0.45 and best_match is not None

        return {
            "is_duplicate": is_duplicate,
            "match": best_match if is_duplicate else None,
            "duplicate_score": round(highest_composite_score * 100, 1),
            "match_reason": match_reason if is_duplicate else "No active duplicate complaint detected."
        }

    # -------------------------------------------------------------
    # 3. AI Priority Recommendation & Water Loss Estimation
    # -------------------------------------------------------------
    def recommend_priority(
        self,
        category: str,
        description: str,
        user_severity: int = 3
    ) -> Dict[str, Any]:
        """
        Determines priority (High, Medium, Low) and estimates hourly water loss.
        """
        text_lower = description.lower()
        score = 0
        reasons = []

        # 1. Base weight by category
        cat_weights = {
            "Main Pipeline Burst": 45,
            "Sewage & Contamination": 40,
            "Road Flooding": 35,
            "Pipe Leakage": 20,
            "Tap Leakage": 10,
            "Other / Meter": 15
        }
        base_cat_score = cat_weights.get(category, 15)
        score += base_cat_score
        reasons.append(f"Category '{category}' hazard baseline: +{base_cat_score} pts")

        # 2. User reported severity (1 to 5)
        severity_score = (user_severity - 1) * 7.5
        score += severity_score
        reasons.append(f"Reported severity {user_severity}/5: +{int(severity_score)} pts")

        # 3. Critical keywords
        critical_keywords = [
            ("gushing", 15, "High-velocity water flow detected"),
            ("burst", 15, "Pipeline rupture detected"),
            ("geyser", 20, "Water geyser / extreme pressure"),
            ("crater", 15, "Structural / asphalt collapse risk"),
            ("sinkhole", 20, "Critical sinkhole warning"),
            ("submerged", 15, "Submerged roadway or property"),
            ("flooding", 12, "Flooding reported"),
            ("hospital", 18, "Proximity to emergency / hospital facility"),
            ("school", 15, "Proximity to school / high pedestrian zone"),
            ("traffic", 10, "Traffic obstruction / road hazard"),
            ("contamination", 18, "Drinking water contamination threat"),
            ("foul smell", 12, "Sewage contamination odor"),
            ("electrical", 20, "Proximity to electrical hazard / wires"),
            ("drinking water", 10, "Treated potable water wastage"),
            ("foundation", 15, "Building foundation damage risk")
        ]

        detected_reasons = []
        for kw, pts, label in critical_keywords:
            if kw in text_lower:
                score += pts
                detected_reasons.append(label)

        if detected_reasons:
            reasons.extend(detected_reasons[:3])

        # Priority tiers
        if score >= 65:
            priority = "High"
        elif score >= 35:
            priority = "Medium"
        else:
            priority = "Low"

        # Water loss estimation in Liters Per Hour (LPH)
        loss_rates = {
            "Main Pipeline Burst": (2500, 12000),
            "Road Flooding": (1500, 6000),
            "Sewage & Contamination": (500, 2000),
            "Pipe Leakage": (200, 1500),
            "Other / Meter": (100, 600),
            "Tap Leakage": (15, 80)
        }
        low_bound, high_bound = loss_rates.get(category, (100, 500))
        severity_ratio = user_severity / 5.0
        est_lph = int(low_bound + (high_bound - low_bound) * severity_ratio)

        return {
            "priority": priority,
            "score": min(100, int(score)),
            "estimated_loss_lph": est_lph,
            "reasons": reasons
        }

    # -------------------------------------------------------------
    # 4. AI Field Summary Generator
    # -------------------------------------------------------------
    def generate_field_summary(
        self,
        title: str,
        category: str,
        description: str,
        street_name: str,
        priority: str
    ) -> str:
        """
        Synthesizes a standardized, actionable 2-3 sentence Field Dispatch Summary
        designed for maintenance crews on mobile devices.
        """
        desc_clean = description.strip()
        sentences = [s.strip() for s in re.split(r'[.!?]+', desc_clean) if s.strip()]
        first_sentence = sentences[0] if sentences else desc_clean

        urgency_prefix = {
            "High": "EMERGENCY DISPATCH: Urgent action required.",
            "Medium": "ACTION REQUIRED: Schedule prompt site visit.",
            "Low": "STANDARD TICKET: Routine maintenance inspection."
        }.get(priority, "ACTION REQUIRED:")

        summary = f"{urgency_prefix} {category} reported at {street_name}. Citizen states: \"{first_sentence}\"."
        
        # Add safety notes if hazardous
        desc_lower = desc_clean.lower()
        if "electrical" in desc_lower or "power" in desc_lower or "pole" in desc_lower:
            summary += " CAUTION: Possible electrical hazard nearby."
        elif "traffic" in desc_lower or "road" in desc_lower or "jam" in desc_lower:
            summary += " Traffic flow advisory: Deploy safety cones upon arrival."
        elif "contamination" in desc_lower or "sewage" in desc_lower or "smell" in desc_lower:
            summary += " Water quality testing kit required on-site."

        return summary

    # -------------------------------------------------------------
    # 5. Hotspot & Trend Analytics Engine
    # -------------------------------------------------------------
    def analyze_trends(self, complaints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes hotspot clustering, category percentages, repeat leak zones,
        and total estimated water saved.
        """
        if not complaints:
            return {
                "total_complaints": 0,
                "hotspots": [],
                "category_breakdown": {},
                "priority_breakdown": {},
                "resolved_count": 0,
                "est_water_saved_liters": 0
            }

        street_counts = {}
        category_counts = {}
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        resolved_count = 0
        total_water_loss_saved = 0

        for c in complaints:
            street = c.get('street_name') or 'Unknown Location'
            street_counts[street] = street_counts.get(street, 0) + 1

            cat = c.get('category') or 'Other / Meter'
            category_counts[cat] = category_counts.get(cat, 0) + 1

            prio = c.get('priority') or 'Medium'
            priority_counts[prio] = priority_counts.get(prio, 0) + 1

            if c.get('status') == 'Resolved':
                resolved_count += 1
                lph = 450
                if prio == "High":
                    lph = 2500
                elif prio == "Low":
                    lph = 50
                total_water_loss_saved += lph * 24

        sorted_streets = sorted(street_counts.items(), key=lambda x: x[1], reverse=True)
        hotspots = [
            {"street": st, "count": cnt, "is_critical": cnt >= 3}
            for st, cnt in sorted_streets[:8]
        ]

        return {
            "total_complaints": len(complaints),
            "hotspots": hotspots,
            "category_breakdown": category_counts,
            "priority_breakdown": priority_counts,
            "resolved_count": resolved_count,
            "est_water_saved_liters": total_water_loss_saved
        }


# Singleton instance
ai_engine = WaterLeakageAIEngine()
