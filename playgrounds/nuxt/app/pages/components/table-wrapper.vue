<script setup lang="ts">
import theme from '#build/b24ui/table-wrapper'

const sizes = Object.keys(theme.variants.size)

const multipleAttrs = reactive({
  size: [theme.defaultVariants.size]
})

const singleAttrs = reactive({
  rounded: false,
  bordered: false,
  zebra: false,
  rowHover: false,
  pinRows: false,
  pinCols: false
})
</script>

<template>
  <PlaygroundPage>
    <template #controls>
      <B24Select v-model="multipleAttrs.size" class="w-32" :items="sizes" placeholder="Size" multiple />
      <B24Switch v-model="singleAttrs.rounded" label="Rounded" />
      <B24Switch v-model="singleAttrs.bordered" label="Bordered" />
      <B24Switch v-model="singleAttrs.zebra" label="Zebra" />
      <B24Switch v-model="singleAttrs.rowHover" label="RowHover" />
      <B24Switch v-model="singleAttrs.pinRows" label="PinRows" />
      <B24Switch v-model="singleAttrs.pinCols" label="PinCols" />
    </template>

    <Matrix v-slot="props" :attrs="multipleAttrs" :b24ui="{ root: 'max-w-250 w-full' }">
      <B24TableWrapper
        class="overflow-x-auto w-full h-[400px]"
        v-bind="{ ...singleAttrs, ...props }"
      >
        <table class="[&_th]:whitespace-nowrap [&_td]:whitespace-nowrap">
          <!-- head -->
          <thead>
            <tr>
              <th>#</th>
              <th>Deal Name</th>
              <th>Company</th>
              <th>Deal Stage</th>
              <th>Amount (USD)</th>
              <th>Assigned To</th>
              <th>Start Date</th>
              <th>Notes</th>
              <th>#</th>
            </tr>
          </thead>
          <tbody>
            <!-- row 1 -->
            <tr>
              <th>1</th>
              <td>Tech Upgrade Project</td>
              <td>Tech Innovators Inc.</td>
              <td>Proposal Sent</td>
              <td>150,000</td>
              <td>John Doe</td>
              <td>01/15/2023</td>
              <td>Waiting for feedback</td>
              <th>1</th>
            </tr>
            <!-- row 2 -->
            <tr>
              <th>2</th>
              <td>Global Expansion Plan</td>
              <td>Global Solutions Ltd.</td>
              <td>Negotiation</td>
              <td>500,000</td>
              <td>Jane Smith</td>
              <td>02/10/2023</td>
              <td>Key decision maker</td>
              <th>2</th>
            </tr>
            <!-- row 3 -->
            <tr>
              <th>3</th>
              <td>New Product Launch</td>
              <td>Future Enterprises</td>
              <td>Contract Signed</td>
              <td>300,000</td>
              <td>Michael Brown</td>
              <td>03/05/2023</td>
              <td>Delivery in progress</td>
              <th>3</th>
            </tr>
            <!-- row 4 -->
            <tr>
              <th>4</th>
              <td>Marketing Campaign</td>
              <td>Bright Ideas Co.</td>
              <td>Initial Contact</td>
              <td>75,000</td>
              <td>Emily Davis</td>
              <td>04/20/2023</td>
              <td>Budget approved</td>
              <th>4</th>
            </tr>
            <!-- row 5 -->
            <tr>
              <th>5</th>
              <td>IT Infrastructure Deal</td>
              <td>NextGen Technologies</td>
              <td>Closing</td>
              <td>1,000,000</td>
              <td>David Wilson</td>
              <td>05/12/2023</td>
              <td>Finalizing details</td>
              <th>5</th>
            </tr>
            <!-- row 6 -->
            <tr>
              <th>6</th>
              <td>HR Software Implementation</td>
              <td>People First Inc.</td>
              <td>Proposal Sent</td>
              <td>200,000</td>
              <td>Sophi Biles</td>
              <td>06/01/2023</td>
              <td>Awaiting approval</td>
              <th>6</th>
            </tr>
            <!-- row 7 -->
            <tr>
              <th>7</th>
              <td>Logistics Optimization</td>
              <td>Logistics Pro</td>
              <td>Negotiation</td>
              <td>450,000</td>
              <td>Reid Semiras</td>
              <td>07/18/2023</td>
              <td>Discussing terms</td>
              <th>7</th>
            </tr>
            <!-- row 8 -->
            <tr>
              <th>8</th>
              <td>Sales Training Program</td>
              <td>Global Sales Ltd.</td>
              <td>Contract Signed</td>
              <td>120,000</td>
              <td>Alec Lethby</td>
              <td>08/22/2023</td>
              <td>Training scheduled</td>
              <th>8</th>
            </tr>
            <!-- row 9 -->
            <tr>
              <th>9</th>
              <td>Product Redesign</td>
              <td>Innovate Corp.</td>
              <td>Initial Contact</td>
              <td>90,000</td>
              <td>Florida Garces</td>
              <td>09/05/2023</td>
              <td>Initial discussions</td>
              <th>9</th>
            </tr>
            <!-- row 10 -->
            <tr>
              <th>10</th>
              <td>Cloud Migration</td>
              <td>Tech Solutions Inc.</td>
              <td>Closing</td>
              <td>600,000</td>
              <td>Maribeth Popping</td>
              <td>10/10/2023</td>
              <td>Final review</td>
              <th>10</th>
            </tr>
          </tbody>
          <!-- head -->
          <thead>
            <tr>
              <th>###</th>
              <th>Old Deal Name</th>
              <th>Old Company</th>
              <th>Old Deal Stage</th>
              <th>Amount (EUR)</th>
              <th>Created By</th>
              <th>End Date</th>
              <th>Old Notes</th>
              <th>###</th>
            </tr>
          </thead>
          <tbody>
            <!-- row 11 -->
            <tr>
              <th>11</th>
              <td>Customer Support Upgrade</td>
              <td>Zemlak, Daniel and Leannon</td>
              <td>Proposal Sent</td>
              <td>85,000</td>
              <td>Hart Hagerty</td>
              <td>11/15/2023</td>
              <td>Pending approval</td>
              <th>11</th>
            </tr>
            <!-- row 12 -->
            <tr>
              <th>12</th>
              <td>Financial Audit</td>
              <td>Carroll Group</td>
              <td>Negotiation</td>
              <td>250,000</td>
              <td>Brice Swyre</td>
              <td>12/01/2023</td>
              <td>Scope finalized</td>
              <th>12</th>
            </tr>
            <!-- row 13 -->
            <tr>
              <th>13</th>
              <td>Office Renovation</td>
              <td>Rowe-Schoen</td>
              <td>Contract Signed</td>
              <td>180,000</td>
              <td>Marjy Ferencz</td>
              <td>01/10/2024</td>
              <td>Work in progress</td>
              <th>13</th>
            </tr>
            <!-- row 14 -->
            <tr>
              <th>14</th>
              <td>Cybersecurity Upgrade</td>
              <td>Wyman-Ledner</td>
              <td>Initial Contact</td>
              <td>300,000</td>
              <td>Yancy Tear</td>
              <td>02/05/2024</td>
              <td>Initial assessment</td>
              <th>14</th>
            </tr>
            <!-- row 15 -->
            <tr>
              <th>15</th>
              <td>Employee Wellness Program</td>
              <td>Schuster-Schimmel</td>
              <td>Closing</td>
              <td>95,000</td>
              <td>Meghann Durtnal</td>
              <td>03/12/2024</td>
              <td>Finalizing details</td>
              <th>15</th>
            </tr>
            <!-- row 16 -->
            <tr>
              <th>16</th>
              <td>Data Analytics Project</td>
              <td>Wiza, Bins and Emard</td>
              <td>Proposal Sent</td>
              <td>220,000</td>
              <td>Irma Vasilik</td>
              <td>04/18/2024</td>
              <td>Awaiting feedback</td>
              <th>16</th>
            </tr>
            <!-- row 17 -->
            <tr>
              <th>17</th>
              <td>E-commerce Platform</td>
              <td>O'Hara, Welch and Keebler</td>
              <td>Negotiation</td>
              <td>700,000</td>
              <td>Sammy Seston</td>
              <td>05/22/2024</td>
              <td>Key terms discussed</td>
              <th>17</th>
            </tr>
            <!-- row 18 -->
            <tr>
              <th>18</th>
              <td>AI Integration</td>
              <td>Turner-Kuhlman</td>
              <td>Contract Signed</td>
              <td>1,200,000</td>
              <td>Lesya Tinham</td>
              <td>06/30/2024</td>
              <td>Implementation started</td>
              <th>18</th>
            </tr>
            <!-- row 19 -->
            <tr>
              <th>19</th>
              <td>Supply Chain Optimization</td>
              <td>Kshlerin, Rogahn and Swaniawski</td>
              <td>Initial Contact</td>
              <td>400,000</td>
              <td>Aland Wilber</td>
              <td>07/15/2024</td>
              <td>Initial discussions</td>
              <th>19</th>
            </tr>
            <!-- row 20 -->
            <tr>
              <th>20</th>
              <td>Product Launch Event</td>
              <td>Sauer LLC</td>
              <td>Closing</td>
              <td>150,000</td>
              <td>Zaneta Tewkesbury</td>
              <td>08/20/2024</td>
              <td>Final preparations</td>
              <th>20</th>
            </tr>
            <!-- row 21 -->
            <tr>
              <th>21</th>
              <td>Mobile App Development</td>
              <td>Hilpert Group</td>
              <td>Proposal Sent</td>
              <td>350,000</td>
              <td>Andy Tipple</td>
              <td>09/25/2024</td>
              <td>Awaiting approval</td>
              <th>21</th>
            </tr>
            <!-- row 22 -->
            <tr>
              <th>22</th>
              <td>Customer Loyalty Program</td>
              <td>Gutmann Inc</td>
              <td>Negotiation</td>
              <td>120,000</td>
              <td>Sophi Biles</td>
              <td>10/10/2024</td>
              <td>Terms under review</td>
              <th>22</th>
            </tr>
            <!-- row 23 -->
            <tr>
              <th>23</th>
              <td>ERP System Implementation</td>
              <td>Gaylord, Pacocha and Baumbach</td>
              <td>Contract Signed</td>
              <td>900,000</td>
              <td>Florida Garces</td>
              <td>11/15/2024</td>
              <td>Project kickoff</td>
              <th>23</th>
            </tr>
            <!-- row 24 -->
            <tr>
              <th>24</th>
              <td>Digital Marketing Campaign</td>
              <td>Deckow-Pouros</td>
              <td>Initial Contact</td>
              <td>200,000</td>
              <td>Maribeth Popping</td>
              <td>12/20/2024</td>
              <td>Initial discussions</td>
              <th>24</th>
            </tr>
            <!-- row 25 -->
            <tr>
              <th>25</th>
              <td>Warehouse Automation</td>
              <td>Schiller, Cole and Hackett</td>
              <td>Closing</td>
              <td>1,500,000</td>
              <td>Moritz Dryburgh</td>
              <td>01/05/2025</td>
              <td>Finalizing details</td>
              <th>25</th>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <th colspan="5" class="text-right">
                Total: 9,825,000
              </th>
              <td colspan="4" />
            </tr>
          </tfoot>
        </table>
      </B24TableWrapper>
    </Matrix>
  </PlaygroundPage>
</template>
