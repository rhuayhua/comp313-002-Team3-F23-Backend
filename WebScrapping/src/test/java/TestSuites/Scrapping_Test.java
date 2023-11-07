package TestSuites;

import PageObjectSteps.BaseTest;
import io.qameta.allure.Epic;
import org.testng.annotations.Test;
import java.io.IOException;

public class Scrapping_Test extends BaseTest {

    @Epic("Landing Test")

    @Test(description = "LT01_GetData", alwaysRun = true, priority = 0, groups = {"Regression"})
    public void LT01_GetData() throws InterruptedException, IOException {
        scrappingSteps.getData("backend developer", "TORONTO");
    }

}
