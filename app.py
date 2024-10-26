import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import random
import plotly.express as px

# Placeholder for fitness tracker API
# import fitness_tracker_api

# Placeholder for food database API
# import food_database_api


FOOD_DATABASE = {
    "Chicken Breast": {
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6,
        "fiber": 0,
        "sugar": 0,
        "sodium": 74,
        "potassium": 256,
        "vitamins": ["B6", "B3"],
    },
    "Brown Rice": {
        "calories": 216,
        "protein": 5,
        "carbs": 45,
        "fat": 1.6,
        "fiber": 3.5,
        "sugar": 0.7,
        "sodium": 10,
        "potassium": 84,
        "vitamins": ["B1", "B6"],
    },
    "Broccoli": {
        "calories": 55,
        "protein": 3.7,
        "carbs": 11.2,
        "fat": 0.6,
        "fiber": 5.1,
        "sugar": 2.6,
        "sodium": 33,
        "potassium": 468,
        "vitamins": ["C", "K"],
    },
    "Salmon": {
        "calories": 206,
        "protein": 22,
        "carbs": 0,
        "fat": 13,
        "fiber": 0,
        "sugar": 0,
        "sodium": 59,
        "potassium": 366,
        "vitamins": ["D", "B12"],
    },
    "Sweet Potato": {
        "calories": 180,
        "protein": 2,
        "carbs": 41.4,
        "fat": 0.1,
        "fiber": 6.6,
        "sugar": 13,
        "sodium": 36,
        "potassium": 475,
        "vitamins": ["A", "C"],
    },
    "Greek Yogurt": {
        "calories": 100,
        "protein": 18,
        "carbs": 6,
        "fat": 0.7,
        "fiber": 0,
        "sugar": 6,
        "sodium": 36,
        "potassium": 141,
        "vitamins": ["B12", "B2"],
    },
    "Spinach": {
        "calories": 23,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 2.2,
        "sugar": 0.4,
        "sodium": 79,
        "potassium": 558,
        "vitamins": ["K", "A"],
    },
}


# Initialize session state for user data if it doesn't exist
if "user_data" not in st.session_state:
    st.session_state.user_data = pd.DataFrame(
        columns=["Date", "Weight", "Body Fat %", "Waist", "Chest", "Arms", "Thighs"]
    )


def main():
    st.title("CalTrack Pro: Your Personal Nutrition Assistant")

    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        [
            "Home",
            "Meal Planner",
            "Nutrient Analysis",
            "Progress Tracking",
            "Fitness Tracker Integration",
        ],
    )

    if page == "Home":
        home_page()
    elif page == "Meal Planner":
        meal_planner_page()
    elif page == "Nutrient Analysis":
        nutrient_analysis_page()
    elif page == "Progress Tracking":
        progress_tracking_page()
    elif page == "Fitness Tracker Integration":
        fitness_tracker_page()


def home_page():
    st.header("Welcome to CalTrack Pro")
    st.write("Track your calories, plan your meals, and achieve your health goals!")

    # User profile
    st.subheader("Your Profile")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=1.0, max_value=300.0, value=170.0)
    activity_level = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extra Active",
        ],
    )

    # Calculate BMR and TDEE
    bmr = calculate_bmr(age, gender, weight, height)
    tdee = calculate_tdee(bmr, activity_level)

    st.write(f"Your Basal Metabolic Rate (BMR): {bmr:.2f} calories/day")
    st.write(f"Your Total Daily Energy Expenditure (TDEE): {tdee:.2f} calories/day")


def meal_planner_page():
    st.header("Personalized Meal Planner")

    # Get user's daily calorie goal
    calorie_goal = st.number_input(
        "Your daily calorie goal", min_value=1000, max_value=5000, value=2000
    )

    # Create tabs for each meal
    tabs = st.tabs(["Breakfast", "Lunch", "Dinner", "Snacks"])

    # Initialize session state for meal plan if it doesn't exist
    if "meal_plan" not in st.session_state:
        st.session_state.meal_plan = {
            meal: [] for meal in ["Breakfast", "Lunch", "Dinner", "Snacks"]
        }

    # Function to add food to a meal
    def add_food(meal):
        food = st.selectbox(
            f"Select food for {meal}",
            options=list(FOOD_DATABASE.keys()),
            key=f"{meal}_food",
        )
        amount = st.number_input(
            f"Amount (grams) for {meal}",
            min_value=1,
            max_value=1000,
            value=100,
            key=f"{meal}_amount",
        )
        if st.button(f"Add to {meal}", key=f"{meal}_add"):
            st.session_state.meal_plan[meal].append((food, amount))
            st.rerun()

    # Function to remove food from a meal
    def remove_food(meal, index):
        st.session_state.meal_plan[meal].pop(index)
        st.rerun()

    # Function to calculate nutritional information for a meal
    def calculate_meal_nutrition(meal_foods):
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for food, amount in meal_foods:
            factor = amount / 100  # Assuming the database values are per 100g
            for nutrient in total:
                total[nutrient] += FOOD_DATABASE[food][nutrient] * factor
        return total

    # Display meal planner for each meal
    for i, meal in enumerate(["Breakfast", "Lunch", "Dinner", "Snacks"]):
        with tabs[i]:
            add_food(meal)
            st.write(f"Your {meal} plan:")
            for idx, (food, amount) in enumerate(st.session_state.meal_plan[meal]):
                st.write(f"- {food}: {amount}g")
                if st.button(f"Remove {food}", key=f"{meal}_remove_{idx}"):
                    remove_food(meal, idx)

            meal_nutrition = calculate_meal_nutrition(st.session_state.meal_plan[meal])
            st.write(f"{meal} nutritional information:")
            st.write(f"Calories: {meal_nutrition['calories']:.1f}")
            st.write(f"Protein: {meal_nutrition['protein']:.1f}g")
            st.write(f"Carbs: {meal_nutrition['carbs']:.1f}g")
            st.write(f"Fat: {meal_nutrition['fat']:.1f}g")

    # Calculate and display total daily nutrition
    total_nutrition = {
        nutrient: sum(
            calculate_meal_nutrition(foods)[nutrient]
            for foods in st.session_state.meal_plan.values()
        )
        for nutrient in ["calories", "protein", "carbs", "fat"]
    }

    st.header("Daily Totals")
    st.write(f"Total Calories: {total_nutrition['calories']:.1f} / {calorie_goal}")
    st.write(f"Total Protein: {total_nutrition['protein']:.1f}g")
    st.write(f"Total Carbs: {total_nutrition['carbs']:.1f}g")
    st.write(f"Total Fat: {total_nutrition['fat']:.1f}g")

    # Progress bar for calorie goal
    progress = total_nutrition["calories"] / calorie_goal
    st.progress(min(progress, 1.0))
    if progress < 1.0:
        st.write(
            f"You have {calorie_goal - total_nutrition['calories']:.1f} calories left for the day."
        )
    elif progress > 1.0:
        st.write(
            f"You've exceeded your calorie goal by {total_nutrition['calories'] - calorie_goal:.1f} calories."
        )

    # Meal plan suggestions
    if st.button("Suggest a meal plan"):
        suggest_meal_plan(calorie_goal)


def suggest_meal_plan(calorie_goal):
    st.subheader("Suggested Meal Plan")
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    meal_ratios = [0.25, 0.35, 0.30, 0.10]  # Approximate calorie distribution

    for meal, ratio in zip(meals, meal_ratios):
        meal_calories = calorie_goal * ratio
        st.write(f"{meal} (Target: {meal_calories:.0f} calories):")

        meal_plan = []
        current_calories = 0

        while current_calories < meal_calories:
            food = random.choice(list(FOOD_DATABASE.keys()))
            amount = random.randint(50, 200)  # Random amount between 50g and 200g
            food_calories = FOOD_DATABASE[food]["calories"] * (amount / 100)

            if (
                current_calories + food_calories <= meal_calories * 1.1
            ):  # Allow 10% overflow
                meal_plan.append((food, amount))
                current_calories += food_calories

            if len(meal_plan) >= 3:  # Limit to 3 items per meal for simplicity
                break

        for food, amount in meal_plan:
            st.write(f"- {food}: {amount}g")

        st.write(f"Total calories: {current_calories:.0f}")
        st.write("")

    st.write("This feature is under development. Check back soon!")


def nutrient_analysis_page():
    st.header("Nutrient Analysis")

    # Tabs for different features
    tabs = st.tabs(["Nutrient Analysis", "Meal Recommendations", "Nutrition Education"])

    with tabs[0]:
        nutrient_analysis()

    with tabs[1]:
        meal_recommendations()

    with tabs[2]:
        nutrition_education()


def nutrient_analysis():
    st.subheader("Nutrient Analysis")

    # Food selection
    selected_food = st.selectbox(
        "Select a food to analyze:", options=list(FOOD_DATABASE.keys())
    )
    amount = st.number_input("Amount (grams):", min_value=1, max_value=1000, value=100)

    if selected_food:
        food_data = FOOD_DATABASE[selected_food]
        st.write(f"Nutritional information for {amount}g of {selected_food}:")

        # Calculate nutrients based on amount
        nutrients = {
            k: v * (amount / 100) for k, v in food_data.items() if k != "vitamins"
        }

        # Create a DataFrame for the nutrient information
        df = pd.DataFrame(list(nutrients.items()), columns=["Nutrient", "Value"])
        df["Value"] = df["Value"].round(2)

        # Display nutrient information as a table
        st.dataframe(df.set_index("Nutrient"), width=500)

        # Create a pie chart for macronutrients
        macros = ["protein", "carbs", "fat"]
        macro_values = [nutrients[m] for m in macros]
        fig = px.pie(
            values=macro_values, names=macros, title="Macronutrient Distribution"
        )
        st.plotly_chart(fig)

        # Display vitamins
        st.write("Vitamins:", ", ".join(food_data["vitamins"]))


def meal_recommendations():
    st.subheader("Meal Recommendations")

    # Get user preferences
    diet_type = st.selectbox(
        "Diet type:", ["Balanced", "High-protein", "Low-carb", "Vegetarian", "Vegan"]
    )
    calorie_target = st.number_input(
        "Daily calorie target:", min_value=1000, max_value=5000, value=2000
    )

    if st.button("Generate Meal Plan"):
        st.write(
            f"Here's a suggested meal plan for a {diet_type} diet with {calorie_target} calories:"
        )

        # This is a simplified meal plan generator. In a real app, you'd use more sophisticated logic.
        meals = ["Breakfast", "Lunch", "Dinner", "Snack"]
        for meal in meals:
            st.write(f"\n{meal}:")
            meal_calories = calorie_target * (
                0.3 if meal != "Snack" else 0.1
            )  # 30% for main meals, 10% for snack
            foods = random.sample(list(FOOD_DATABASE.keys()), 3)
            for food in foods:
                amount = round(
                    meal_calories / (len(foods) * FOOD_DATABASE[food]["calories"]) * 100
                )
                st.write(f"- {amount}g of {food}")

        st.write(
            "\nNote: This is a basic suggestion. Please consult with a nutritionist for a personalized meal plan."
        )


def nutrition_education():
    st.subheader("Nutrition Education")

    # Educational topics
    topics = [
        "Understanding Macronutrients",
        "The Importance of Micronutrients",
        "Healthy Eating Habits",
        "Reading Nutrition Labels",
        "The Role of Fiber in Diet",
    ]

    selected_topic = st.selectbox("Choose a topic to learn about:", topics)

    if selected_topic == "Understanding Macronutrients":
        st.write("""
        Macronutrients are the nutrients that your body needs in large amounts:

        1. Proteins: Essential for building and repairing tissues.
        2. Carbohydrates: The body's main source of energy.
        3. Fats: Important for nutrient absorption, nerve transmission, and maintaining cell membranes.

        A balanced diet typically includes all three macronutrients in appropriate proportions.
        """)

    elif selected_topic == "The Importance of Micronutrients":
        st.write("""
        Micronutrients are vitamins and minerals that your body needs in smaller amounts:

        - Vitamins: Organic compounds needed for various bodily functions.
        - Minerals: Inorganic elements that play crucial roles in bodily processes.

        While needed in smaller quantities, micronutrients are essential for overall health and well-being.
        """)

    elif selected_topic == "Healthy Eating Habits":
        st.write("""
        Developing healthy eating habits is crucial for maintaining good health:

        1. Eat a variety of foods from all food groups.
        2. Control portion sizes.
        3. Choose whole grains over refined grains.
        4. Include plenty of fruits and vegetables in your diet.
        5. Limit processed foods and added sugars.
        6. Stay hydrated by drinking plenty of water.
        7. Practice mindful eating.
        """)

    elif selected_topic == "Reading Nutrition Labels":
        st.write("""
        Understanding nutrition labels can help you make informed food choices:

        1. Check the serving size and servings per container.
        2. Look at the calorie content.
        3. Pay attention to the % Daily Value (%DV).
        4. Limit saturated fats, trans fats, cholesterol, and sodium.
        5. Ensure you're getting enough fiber, vitamins, and minerals.
        6. Check the ingredient list for added sugars and unhealthy additives.
        """)

    elif selected_topic == "The Role of Fiber in Diet":
        st.write("""
        Fiber is a type of carbohydrate that the body can't digest. It's important because it:

        1. Promotes regular bowel movements and prevents constipation.
        2. Helps maintain bowel health.
        3. Lowers cholesterol levels.
        4. Helps control blood sugar levels.
        5. Aids in achieving a healthy weight.

        Good sources of fiber include fruits, vegetables, whole grains, and legumes.
        """)

    st.write("This feature is under development. Check back soon!")


def progress_tracking_page():
    st.header("Progress Tracking")

    # Tabs for different features
    tabs = st.tabs(["Log Progress", "View Progress", "Set Goals"])

    with tabs[0]:
        log_progress()

    with tabs[1]:
        view_progress()

    with tabs[2]:
        set_goals()


def log_progress():
    st.subheader("Log Your Progress")

    # Date selection (default to today)
    date = st.date_input("Date", datetime.now())

    # Input fields for various measurements
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1)
    body_fat = st.number_input("Body Fat %", min_value=0.0, max_value=100.0, step=0.1)
    waist = st.number_input(
        "Waist Circumference (cm)", min_value=0.0, max_value=200.0, step=0.1
    )
    chest = st.number_input(
        "Chest Circumference (cm)", min_value=0.0, max_value=200.0, step=0.1
    )
    arms = st.number_input(
        "Arm Circumference (cm)", min_value=0.0, max_value=100.0, step=0.1
    )
    thighs = st.number_input(
        "Thigh Circumference (cm)", min_value=0.0, max_value=200.0, step=0.1
    )

    if st.button("Log Progress"):
        new_data = pd.DataFrame(
            {
                "Date": [date],
                "Weight": [weight],
                "Body Fat %": [body_fat],
                "Waist": [waist],
                "Chest": [chest],
                "Arms": [arms],
                "Thighs": [thighs],
            }
        )
        st.session_state.user_data = pd.concat(
            [st.session_state.user_data, new_data], ignore_index=True
        )
        st.success("Progress logged successfully!")


def view_progress():
    st.subheader("View Your Progress")

    if st.session_state.user_data.empty:
        st.warning("No data available. Please log your progress first.")
        return

    # Sort data by date
    st.session_state.user_data["Date"] = pd.to_datetime(
        st.session_state.user_data["Date"]
    )
    st.session_state.user_data = st.session_state.user_data.sort_values("Date")

    # Select metric to view
    metric = st.selectbox(
        "Select metric to view:", st.session_state.user_data.columns[1:]
    )

    # Create line chart
    fig = px.line(
        st.session_state.user_data, x="Date", y=metric, title=f"{metric} Over Time"
    )
    st.plotly_chart(fig)

    # Display data table
    st.dataframe(st.session_state.user_data)

    # Calculate and display changes
    if len(st.session_state.user_data) > 1:
        first_entry = st.session_state.user_data.iloc[0]
        last_entry = st.session_state.user_data.iloc[-1]

        st.subheader("Overall Changes")
        for column in st.session_state.user_data.columns[1:]:
            change = last_entry[column] - first_entry[column]
            st.write(f"{column}: {change:.2f}")


def set_goals():
    st.subheader("Set Your Goals")

    # Initialize goals in session state if they don't exist
    if "goals" not in st.session_state:
        st.session_state.goals = {}

    # Input fields for goals
    st.session_state.goals["target_weight"] = st.number_input(
        "Target Weight (kg)",
        min_value=0.0,
        max_value=500.0,
        step=0.1,
        value=st.session_state.goals.get("target_weight", 0.0),
    )
    st.session_state.goals["target_body_fat"] = st.number_input(
        "Target Body Fat %",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        value=st.session_state.goals.get("target_body_fat", 0.0),
    )
    st.session_state.goals["target_date"] = st.date_input(
        "Target Date",
        min_value=datetime.now(),
        value=st.session_state.goals.get(
            "target_date", datetime.now() + timedelta(days=30)
        ),
    )

    if st.button("Set Goals"):
        st.success("Goals set successfully!")

    # Display current goals
    st.subheader("Current Goals")
    for goal, value in st.session_state.goals.items():
        st.write(f"{goal.replace('_', ' ').title()}: {value}")

    # Calculate and display progress towards goals
    if (
        not st.session_state.user_data.empty
        and "target_weight" in st.session_state.goals
    ):
        current_weight = st.session_state.user_data["Weight"].iloc[-1]
        start_weight = st.session_state.user_data["Weight"].iloc[0]
        target_weight = st.session_state.goals["target_weight"]

        if start_weight != target_weight:
            progress = (
                (start_weight - current_weight) / (start_weight - target_weight) * 100
            )
            st.subheader("Progress Towards Weight Goal")
            st.progress(min(progress / 100, 1.0))
            st.write(f"{progress:.1f}% towards your weight goal")

    st.write("This feature is under development. Check back soon!")


def fitness_tracker_page():
    st.header("Fitness Tracker Integration")


# Mock fitness tracker API
class MockFitnessTracker:
    def __init__(self):
        self.connected = False
        self.data = pd.DataFrame(
            columns=["Date", "Steps", "Calories Burned", "Active Minutes", "Heart Rate"]
        )

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def is_connected(self):
        return self.connected

    def get_data(self, days=7):
        if not self.connected:
            return None

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")

        data = []
        for date in date_range:
            data.append(
                {
                    "Date": date,
                    "Steps": random.randint(5000, 15000),
                    "Calories Burned": random.randint(1800, 3000),
                    "Active Minutes": random.randint(30, 120),
                    "Heart Rate": random.randint(60, 100),
                }
            )

        self.data = pd.DataFrame(data)
        return self.data


# Initialize fitness tracker in session state if it doesn't exist
if "fitness_tracker" not in st.session_state:
    st.session_state.fitness_tracker = MockFitnessTracker()


def fitness_tracker_page():
    st.header("Fitness Tracker Integration")

    # Tabs for different features
    tabs = st.tabs(["Connect Device", "Activity Dashboard", "Sync Data"])

    with tabs[0]:
        connect_device()

    with tabs[1]:
        activity_dashboard()

    with tabs[2]:
        sync_data()


def connect_device():
    st.subheader("Connect Your Fitness Tracker")

    if st.session_state.fitness_tracker.is_connected():
        st.success("Your fitness tracker is connected!")
        if st.button("Disconnect Device"):
            st.session_state.fitness_tracker.disconnect()
            st.rerun()
    else:
        st.warning("No fitness tracker connected.")
        if st.button("Connect Device"):
            st.session_state.fitness_tracker.connect()
            st.rerun()


def activity_dashboard():
    st.subheader("Activity Dashboard")

    if not st.session_state.fitness_tracker.is_connected():
        st.warning("Please connect your fitness tracker to view the dashboard.")
        return

    # Get data from the mock fitness tracker
    data = st.session_state.fitness_tracker.get_data()

    if data is None or data.empty:
        st.warning("No data available. Please sync your device.")
        return

    # Display summary statistics
    st.write("Summary (Last 7 Days):")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg. Daily Steps", f"{data['Steps'].mean():.0f}")
    with col2:
        st.metric("Avg. Calories Burned", f"{data['Calories Burned'].mean():.0f}")
    with col3:
        st.metric("Avg. Active Minutes", f"{data['Active Minutes'].mean():.0f}")

    # Create line charts
    metrics = ["Steps", "Calories Burned", "Active Minutes", "Heart Rate"]
    for metric in metrics:
        fig = px.line(data, x="Date", y=metric, title=f"{metric} Over Time")
        st.plotly_chart(fig)


def sync_data():
    st.subheader("Sync Fitness Data")

    if not st.session_state.fitness_tracker.is_connected():
        st.warning("Please connect your fitness tracker to sync data.")
        return

    if st.button("Sync Now"):
        with st.spinner("Syncing data..."):
            # Simulate syncing delay
            import time

            time.sleep(2)

            # Get new data
            new_data = st.session_state.fitness_tracker.get_data()

            # Update calorie goal based on activity level
            avg_calories_burned = new_data["Calories Burned"].mean()
            if "calorie_goal" not in st.session_state:
                st.session_state.calorie_goal = 2000  # Default goal

            if avg_calories_burned > 2500:
                st.session_state.calorie_goal += 200
            elif avg_calories_burned < 2000:
                st.session_state.calorie_goal -= 100

            st.success("Data synced successfully!")
            st.write(
                f"Your new daily calorie goal is: {st.session_state.calorie_goal} calories"
            )

    if "calorie_goal" in st.session_state:
        st.write(
            f"Current daily calorie goal: {st.session_state.calorie_goal} calories"
        )

    # Display sync history (for demonstration, we'll just show the last sync time)
    if "last_sync" not in st.session_state:
        st.session_state.last_sync = None

    if st.session_state.last_sync:
        st.write(f"Last synced: {st.session_state.last_sync}")

    st.session_state.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.write("This feature is under development. Check back soon!")


def calculate_bmr(age, gender, weight, height):
    if gender == "Male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "Female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        return (
            88.362
            + (13.397 * weight)
            + (4.799 * height)
            - (5.677 * age)
            + 447.593
            + (9.247 * weight)
            + (3.098 * height)
            - (4.330 * age)
        ) / 2


def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9,
    }
    return bmr * activity_factors[activity_level]


if __name__ == "__main__":
    main()
