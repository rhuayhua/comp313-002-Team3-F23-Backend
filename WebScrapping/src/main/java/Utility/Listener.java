package Utility;

import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

public class Listener implements ITestListener {

    @Override
    public void onTestStart(ITestResult result) {
        printDebugMessage(result.getMethod().getTestClass() + "-" + result.getMethod().getDescription() + " - onTestStart, SessionID: " + ((RemoteWebDriver) BasePage.getDriver()).getSessionId());
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        printDebugMessage(result.getMethod().getTestClass() + "-" + result.getMethod().getDescription() + " - onTestSuccess, SessionID: " + ((RemoteWebDriver) BasePage.getDriver()).getSessionId());
    }

    @Override
    public void onTestFailure(ITestResult result) {
        printDebugMessage(result.getMethod().getTestClass() + "-" + result.getMethod().getDescription() + " - onTestFailure, SessionID: " + ((RemoteWebDriver) BasePage.getDriver()).getSessionId());
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        printDebugMessage("onTestSkipped");
    }

    @Override
    public void onTestFailedButWithinSuccessPercentage(ITestResult result) {
        printDebugMessage("onTestFailedButWithinSuccessPercentage");
    }

    @Override
    public void onTestFailedWithTimeout(ITestResult result) {
        printDebugMessage("onTestFailedWithTimeout");
    }

    @Override
    public void onStart(ITestContext context) {
        printDebugMessage("onStart");
    }

    @Override
    public void onFinish(ITestContext context) {
        printDebugMessage("onFinish");
    }

    public void printDebugMessage (String msg) {
        System.out.println("Thread" + Thread.currentThread().getId() + " " + msg);
    }
}

