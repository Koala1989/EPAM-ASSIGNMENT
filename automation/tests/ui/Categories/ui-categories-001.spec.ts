// case: test-cases/Categories/category-hierarchy-and-filtering.md (UI-Categories-001)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('category 001',()=>{
    test('Ui-category-001: verify that user can opena category ',{tag:['@smoke','@regression']},async({data,partsPage,envData})=>{
    
    await   test.step('1. open the part page and click on the part name',async()=>{
        await partsPage.open();
        await partsPage.openPart(envData.part.Displayname);
        // await partsPage.clickPartNameInModal(envData.part.Displayname);

        // await partsPage.openCategoryFromPartPage();

        await expect(partsPage.page).toHaveTitle(new RegExp(`Part: ${envData.part.Displayname}$`));
       }) 

    }
)
})
