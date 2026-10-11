function validateForm() {

    let age = document.forms["loanForm"]["age"].value;
    let income = document.forms["loanForm"]["income"].value;
    let credit = document.forms["loanForm"]["credit_score"].value;

    if (age < 18) {
        alert("Age must be at least 18 years.");
        return false;
    }

    if (income <= 0) {
        alert("Please enter a valid monthly income.");
        return false;
    }

    if (credit < 300 || credit > 900) {
        alert("Credit score must be between 300 and 900.");
        return false;
    }

    return true;
}